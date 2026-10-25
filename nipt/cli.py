from pathlib import Path
import argparse
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from threadpoolctl import threadpool_limits
from .data import load_data
from .analysis import fit_relationship, individual_times, predict_crossing
from .grouping import search_groups

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description='Competition questions 1-3, with explicit data provenance.')
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--data', type=Path)
    parser.add_argument('--out', type=Path, default=ROOT/'artifacts/latest')
    args = parser.parse_args()
    if (not args.demo and args.data is None) or (args.demo and args.data is not None):
        parser.error('Choose exactly one of --demo or --data PATH.')
    threadpool_limits(1)
    df = load_data(ROOT/'data/demo/male_synthetic.csv' if args.demo else args.data)
    args.out.mkdir(parents=True,exist_ok=True)
    clean, fit = fit_relationship(df, optimizer='lbfgs' if args.demo else None)
    (args.out/'mixed_model.txt').write_text(str(fit.summary())+'\nConverged: '+str(fit.converged))
    patient = df.dropna(subset=['patient_id','y_fraction','bmi']).groupby('patient_id').agg(y_mean=('y_fraction','mean'),bmi_mean=('bmi','mean'))
    patient['bmi_band'] = (patient.bmi_mean//5*5).astype(int)
    patient.groupby('bmi_band').agg(patients=('y_mean','size'),mean_y_fraction=('y_mean','mean')).to_csv(args.out/'q1_bmi_summary.csv')
    groups, grouping = search_groups(individual_times(clean,fit))
    groups.to_csv(args.out/'q2_groups.csv',index=False)
    (args.out/'q2_metrics.json').write_text(json.dumps(grouping,indent=2))
    metrics, prediction, mean_groups = predict_crossing(df)
    prediction.to_csv(args.out/'q3_predictions.csv',index=False)
    mean_groups.to_csv(args.out/'q3_bmi_predictions.csv',index=False)
    (args.out/'q3_metrics.json').write_text(json.dumps(metrics,indent=2))
    (args.out/'run.json').write_text(json.dumps({'dataset_kind':'synthetic_demo' if args.demo else 'user_supplied',
                                               'rows':len(df),'patients':df.patient_id.nunique(),
                                               'mixed_model_converged':bool(fit.converged),
                                               'mixed_model_optimizer':'lbfgs' if args.demo else 'source default',
                                               'questions':[1,2,3]},indent=2))
    fig, ax = plt.subplots(figsize=(6,5))
    ax.scatter(prediction.actual_week,prediction.predicted_week,alpha=.65,color='#0891b2',s=25)
    low, high = prediction.actual_week.min(), prediction.actual_week.max()
    ax.plot([low,high],[low,high],color='#94a3b8',ls='--')
    ax.set(xlabel='Simulated crossing-week target',ylabel='Prediction',
           title='Question 3' + (' / SYNTHETIC DEMO' if args.demo else '') + f' / MAE {metrics["mae_weeks"]:.2f} weeks')
    fig.tight_layout();fig.savefig(args.out/'q3_prediction.png',dpi=150);plt.close(fig)
    print(f'Q1 converged: {fit.converged}; Q2 groups: {grouping["groups"]}; Q3 MAE: {metrics["mae_weeks"]:.6f} weeks')
    print(f'Outputs: {args.out}')
