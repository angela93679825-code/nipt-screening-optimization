# Input schema

| Field | Meaning |
|---|---|
| patient_id | Stable group ID for repeated measurements |
| age | Maternal age in years |
| height | Height in cm |
| weight | Weight in kg |
| gestational_age | String such as 12w+6; days are divided by seven |
| pregnancies | Source pregnancy-count field |
| births | Source birth-count field |
| bmi | Source BMI |
| y_fraction | Y-chromosome fraction as a proportion; threshold 0.04 |

The importer reads `男胎检测数据` explicitly. Date of last period, test date, unused sequencing fields and outcomes are omitted from this project input. Group IDs are replaced deterministically while preserving lexical group order, because that order affects the original Monte Carlo random-number sequence. This is a local preparation step, not a guarantee of anonymization.

`data/demo/male_synthetic.csv` is independently generated and contains no original patient rows. The supplied source workbook and all local prepared records are excluded from the upload package and Git.
