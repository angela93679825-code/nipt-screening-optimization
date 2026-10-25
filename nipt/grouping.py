from itertools import combinations
import numpy as np
import pandas as pd


def search_groups(individual):
    """Word question 2 score, not an independently validated clinical objective."""
    data = individual.copy()
    data['adjusted_week'] = data.crossing_week.apply(lambda x:12 if x<5 else 25 if x>30 else x)
    bmi, time = data.bmi.to_numpy(), data.adjusted_week.to_numpy()
    low, high = bmi.min(), bmi.max()
    candidates = np.round(np.linspace(max(18,round(low)), min(41,round(high)),20),1)
    best = None
    valid_count = 0
    for k in [3,4]:
        for cuts in combinations(candidates,k-1):
            edges = np.r_[low, np.sort(cuts), high]
            if np.any(np.diff(edges)<=0):
                continue
            assignment = np.searchsorted(edges[1:-1], bmi, side='right')
            sizes = np.bincount(assignment,minlength=k)
            if (sizes==0).any():
                continue
            grouped = [time[assignment==g] for g in range(k)]
            medians = np.array([np.median(g) for g in grouped])
            coverage = np.mean(time <= medians[assignment]+1.5)
            distinctness = np.diff(np.sort(medians)).mean()
            imbalance = np.maximum(0,sizes/len(data)-.4).sum()
            size_std = sizes.std()/sizes.mean()
            widths = np.diff(edges)
            penalty = .3*(imbalance+size_std) + .2*(widths.max()/widths.mean()-1)
            score = 2*coverage + distinctness - penalty
            valid_count += 1
            if best is None or score > best['score']:
                best = {'k':k,'edges':edges,'times':medians,'sizes':sizes,
                        'coverage':coverage,'score':score,'assignment':assignment}
    if best is None:
        raise ValueError('No valid three/four-group scheme under original search settings.')
    table = pd.DataFrame({'bmi_lower':best['edges'][:-1], 'bmi_upper':best['edges'][1:],
                          'patients':best['sizes'],'algorithm_output_week':best['times']})
    # Retain both source definitions: the Word score and its different exported flag.
    symmetric = np.mean(abs(time-best['times'][best['assignment']])<=1.5)
    summary = {'groups':int(best['k']),'score':float(best['score']),
               'coverage_as_scored':float(best['coverage']),
               'coverage_absolute_difference':float(symmetric),
               'candidate_schemes':valid_count,
               'objective':'historical competition score; not clinical validation'}
    return table, summary
