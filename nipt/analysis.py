import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor

FEATURES = ['age','height','weight','pregnancies','births','pregnancies_minus_births','bmi']


def fit_relationship(frame, optimizer=None):
    """Word source: random intercept and gestational-age random slope."""
    data = frame.dropna(subset=['patient_id','y_fraction','ga','bmi']).copy()
    # The original Word casts these columns to float32 before fitting.
    for col in ['y_fraction','ga','bmi']:
        data[col] = data[col].astype(np.float32)
    model = smf.mixedlm('y_fraction ~ ga + bmi', data=data,
                        groups=data.patient_id, re_formula='ga')
    result = model.fit(maxiter=2000, **({'method': optimizer} if optimizer else {}))
    return data, result


def individual_times(frame, result):
    """Retain the source's threshold-crossing approximation and clipping."""
    mothers = frame[['patient_id','bmi']].drop_duplicates('patient_id')
    fe = result.fe_params
    records = []
    for row in mothers.itertuples(index=False):
        random = result.random_effects.get(row.patient_id)
        intercept = float(random.iloc[0]) if random is not None else 0.
        slope = float(random.iloc[1]) if random is not None and len(random)>1 else 0.
        denom = fe['ga'] + slope
        week = (.04-fe['Intercept']-intercept-fe['bmi']*row.bmi)/denom if abs(denom)>1e-6 else 18.
        records.append({'patient_id':row.patient_id,'bmi':row.bmi,'crossing_week':float(np.clip(week,0,40))})
    return pd.DataFrame(records)


def predict_crossing(frame):
    """Question 3: preserve source ordering, Monte Carlo and patient aggregation."""
    df = frame.copy()
    df['pregnancies'] = pd.to_numeric(df.pregnancies, errors='coerce').fillna(1)
    df['births'] = pd.to_numeric(df.births, errors='coerce').fillna(0)
    df['pregnancies'] = df.pregnancies.apply(lambda x: 3 if x >= 3 else x)
    df['pregnancies_minus_births'] = df.pregnancies - df.births
    rng = np.random.RandomState(42)
    simulated = []
    for patient, group in df.groupby('patient_id'):
        ga, y = group.ga.to_numpy(), group.y_fraction.to_numpy()
        first = []
        for _ in range(100):
            noisy = y + rng.normal(0, .005, size=len(y))
            indices = np.where(noisy >= .04)[0]
            first.append(ga[indices[0]] if len(indices) else np.nan)
        valid = np.asarray(first)[np.isfinite(first)]
        simulated.append({'patient_id':patient,'crossing_week':float(np.median(valid)) if len(valid) else np.nan})
    features = df.groupby('patient_id').first().reset_index().merge(pd.DataFrame(simulated),on='patient_id')
    features = features.dropna(subset=['crossing_week'])
    train, test = train_test_split(features.index, test_size=.2, random_state=42)
    model = XGBRegressor(n_estimators=200, learning_rate=.1, random_state=42, n_jobs=1)
    model.fit(features.loc[train, FEATURES], features.loc[train,'crossing_week'])
    prediction = model.predict(features.loc[test, FEATURES])
    actual = features.loc[test,'crossing_week']
    metrics = {'mae_weeks':float(mean_absolute_error(actual,prediction)),
               'patients':len(features),'train':len(train),'test':len(test),'features':FEATURES}
    features['bmi_group'] = features.bmi.apply(lambda b:'underweight' if b<18.5 else 'normal' if b<24 else 'overweight' if b<28 else 'obese')
    groups = []
    for label, group in features.groupby('bmi_group', sort=False):
        groups.append({'bmi_group':label,'patients':len(group),
                       'predicted_mean_week':float(model.predict(group[FEATURES]).mean())})
    return metrics, pd.DataFrame({'actual_week':actual.to_numpy(),'predicted_week':prediction}), pd.DataFrame(groups)
