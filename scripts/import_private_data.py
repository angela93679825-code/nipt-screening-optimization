"""Read only the male sheet, remove unused fields and hash grouping IDs locally."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nipt.data import COLUMNS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workbook',type=Path,required=True)
    parser.add_argument('--out',type=Path,default=Path('data/private/male.csv'))
    args = parser.parse_args()
    df = pd.read_excel(args.workbook,sheet_name='男胎检测数据',usecols=list(COLUMNS)).rename(columns=COLUMNS)
    # Prefix + hash keeps group identity without embedding the original IDs.
    # Original lexical group order is preserved by a deterministic ordered lookup.
    ordered = sorted(df.patient_id.dropna().unique())
    mapping = {value:f'P{i:04d}_'+hashlib.sha256(str(value).encode()).hexdigest()[:8] for i,value in enumerate(ordered)}
    df.patient_id = df.patient_id.map(mapping)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(args.out,index=False)
    args.out.with_suffix('.provenance.json').write_text(json.dumps({'source_sheet':'男胎检测数据',
                                                                'rows':len(df),'patients':len(ordered),
                                                                'fields':list(df.columns)},indent=2))
    print(f'Prepared local male dataset: {args.out}')


if __name__ == '__main__':
    main()
