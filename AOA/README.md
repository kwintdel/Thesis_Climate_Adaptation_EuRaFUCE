# Area of application (AOA)
Information about how this directory is organised and in what order certain code should be run.
Information about dependencies can be found in the subdirectory 'jobs', where the necessary modules for each code file are defined. 
The subdirectory 'data' contains the importances for each of the Eu-RaFUCE submodels.
This directory contains information about how the DI thresholds for the AOA were made for the Eu-RaFUCE model, so that it can be easily adapted for other models, as well as code which shows how to evaluate the AOA for new data.

## Making the thresholds

### Average distance
1) the make_weights.py should be run to get the weights used by each model. Otherwise the weights from the Eu-RaFUCE model is already present in the 'data' subdirectory.

2) AOA_train_val_folds.py should be run to get one .csv file per cluster model with all train and test data and a fold .csv stating whether a certain row comes from a test city or not.

3) When all previous code is run and cities are divided into clusters, the following code can be run to obtain the average distances and runtimes for different sample sizes for each cluster. This code can easily be adapted to only calculate one sample size:
    - make_DI1_avrgdist.R
    - make_DI2_avrgdist.R
    - make_DI3_avrgdist.R

### Minimal distances and construction thresholds




