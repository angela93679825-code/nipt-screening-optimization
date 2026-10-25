# Provenance and reconstruction

Sources: the user-supplied 2025 national mathematical modeling competition paper, the C-question statement, the original attachment workbook and `代码(1).docx`.

The fuller Word source confirmed question 3's feature list and supplied question 2's grouping search that was incomplete in the PDF appendix. Formatting, desktop paths and damaged indentation were repaired, then the implemented parts were refactored into English-named modules. Question 2's DataFrame covariance indexing was made explicit. Plot labels and result exports are English in this version.

Question 2 still uses the historical score, threshold approximation, clipping and asymmetric coverage definition. The available raw male worksheet is substituted for the named merged workbook that was not supplied; this difference is documented rather than hidden. The module emits both score coverage and the separate absolute-difference coverage.

Question 3 retains the 100-draw simulation, standard deviation 0.005, threshold 0.04, seed 42, patient aggregation, seven predictors, 200 estimators and learning rate 0.1. Source group order is preserved by the importer. MAE is evaluated after a patient-level split.

The original work was a team project. Individual code ownership and team task allocation were not recoverable from the supplied files, so they are not invented here. The original manuscript is not republished in this repository.

For the independent synthetic demo, the same mixed-effects equation is fitted with L-BFGS explicitly; the source-default optimizer sequence is retained for original-data runs. The optimizer choice is recorded in run.json. Boundary warnings are not suppressed.
