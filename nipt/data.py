import pandas as pd
import numpy as np
import re

COLUMNS = {'孕妇代码':'patient_id', '年龄':'age', '身高':'height', '体重':'weight',
           '检测孕周':'gestational_age', '怀孕次数':'pregnancies', '生产次数':'births',
           '孕妇BMI':'bmi', 'Y染色体浓度':'y_fraction'}
REQUIRED = list(COLUMNS.values())


def parse_ga(value):
    match = re.match(r'(\d+)w(?:\+(\d+))?', str(value))
    return int(match.group(1)) + (int(match.group(2)) if match.group(2) else 0)/7 if match else np.nan


def load_data(path):
    frame = pd.read_csv(path, dtype={'patient_id': str})
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    frame['ga'] = frame.gestational_age.apply(parse_ga)
    for col in ['age','height','weight','bmi','y_fraction']:
        frame[col] = pd.to_numeric(frame[col], errors='coerce')
    if frame.patient_id.isna().any():
        raise ValueError('Missing patient IDs; group identity is required.')
    return frame
