"""Generate independent synthetic repeated-measurement records, not real patients."""
from pathlib import Path
import numpy as np
import pandas as pd
import json
rng=np.random.default_rng(2025);records=[]
for i in range(100):
 bmi=rng.uniform(22,44);height=rng.uniform(150,176);age=int(rng.integers(22,42))
 pregnancies=int(rng.integers(1,5));births=int(rng.integers(0,pregnancies))
 intercept=rng.normal(0,.008);slope=rng.normal(0,.00035)
 for ga in [10.5,13,15.5,18,20.5]:
  ga=ga+rng.uniform(-.2,.2);weeks=int(ga);days=int(round((ga-weeks)*7))
  if days==7:weeks+=1;days=0
  actual_ga=weeks+days/7
  y=.018+.0033*(actual_ga-10)-.0007*(bmi-30)+intercept+slope*(actual_ga-15)+rng.normal(0,.004)
  records.append({'patient_id':f'SYN{i:04d}','age':age,'height':height,'weight':bmi*(height/100)**2,
                  'gestational_age':f'{weeks}w+{days}','pregnancies':pregnancies,'births':births,
                  'bmi':bmi,'y_fraction':float(np.clip(y,.001,.18))})
root=Path(__file__).resolve().parents[1]/'data/demo';root.mkdir(parents=True,exist_ok=True)
pd.DataFrame(records).to_csv(root/'male_synthetic.csv',index=False)
(root/'metadata.json').write_text(json.dumps({'dataset_kind':'synthetic_demo','seed':2025,'patients':100,
                                            'contains_original_patient_data':False,'generator':'scripts/generate_demo.py'},indent=2))
