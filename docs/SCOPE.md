# Scope and fourth-question status

The repository's implemented scope is questions 1-3.

The provided Word source and PDF appendix for question 4 construct `X` with `np.random.rand(121, 3)` and manually create four label counts. The Excel DataFrame is not used to build model features or labels. The code also applies SMOTE before splitting the data and does not explicitly select the female worksheet. Fixing indentation would only make a synthetic demonstration executable.

The current files do not establish whether a real-data implementation existed separately or whether demonstration code was pasted into the document. Accordingly, this repository does not claim to reproduce real female abnormality classification, does not include those reported scores, and does not present a newly built classifier as the original method.

A later implementation would need an explicit feature/label mapping, treatment of simultaneous T13/T18/T21 labels, patient-separated evaluation and training-only resampling. That would be a separately documented extension.
