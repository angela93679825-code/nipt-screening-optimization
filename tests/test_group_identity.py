import unittest
import numpy as np
import pandas as pd
from nipt.data import parse_ga
from nipt.grouping import search_groups


class ResearchRules(unittest.TestCase):
    def test_gestational_days_are_sevenths_not_decimal_tenths(self):
        self.assertAlmostEqual(parse_ga('12w+6'),12+6/7)
        self.assertTrue(np.isnan(parse_ga('missing')))

    def test_group_search_accounts_for_all_patients_including_upper_edge(self):
        frame = pd.DataFrame({'patient_id':range(30),'bmi':np.linspace(21,45,30),
                              'crossing_week':np.linspace(11,20,30)})
        groups, metrics = search_groups(frame)
        self.assertEqual(groups.patients.sum(),len(frame))
        self.assertEqual(groups.bmi_upper.iloc[-1],45)
        self.assertIn(metrics['groups'],[3,4])


if __name__ == '__main__':
    unittest.main()
