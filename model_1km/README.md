# model 1km
Information about how this directory is organised and in what order certain code should be run.
Information about dependencies can be found in the subdirectory 'jobs', where the necessary modules for each code file are defined. 
This directory contains files to make the data used to train and evaluate Eu-RaFUCE1km perc and Eu-RaFUCE1km mode models. Files specific for the Eu-RaFUCE1km perc model use the suffix '_interp' as the ERA data is interpolated as well as the percentage of CORINE cover is taken. All other files are necessary for both or only Eu-RaFUCE1km mode. 
Make sure to adjust the file paths accordingly, the code is not made fully optimal to use outside of the Ghent University Tier 2 infrastructure.
The models made during the thesis 'Effect of climate adaptation measures in European cities according to the Eu-RaFUCE model' can be found in the subdirectory 'models'.

1) the makeraster.py should be run to generate the 1km resolution rasters

2) The following list of python files can all be run at the same time and are needed to calculate separate grids for eacht city for this variable:
    - raster_coast.py
    - raster_CORINE.py
    - raster_elev_DMET.py
    - raster_elevation.py
    - raster_ERA_RH.py
    - raster_ERA_RH_interp.py
    - raster_ERA_solar.py
    - raster_ERA_solar_interp.py
    - raster_height.py
    - raster_imperv.py
    - raster_population.py
    - raster_geopotential.py
    - create_training_separate.py

3) Now the Rh, other ERA and UrbClim prediction values can be made into a file per city (previously multiple files were made per month for each city, you can also use those files if you want to only use one month of data for predictions):
    - raster_ERA_RH_percity.py
    - raster_ERA_RH_interp_percity.py
    - raster_ERA_solar_percity.py
    - raster_ERA_solar_interp_percity.py
    - create_training_percity.py

4) All separate rasters can be combined into .csv files using raster_total.py or raster_total_ERA_interp.py for Eu-RaFUCE1km perc or raster_total_no_subsampling.py if you do not want to subsample.

5) After extracting the names of the cities which should be used for training, validation and testing with train_val_cities.py, the subsampled total rasters can be combined into training, validation and test set using:
    - create_train_val_cluster.py
    - creaste_train_val_cluster_ERA_interp.py

6) Now the models can be trained, using the following files:
    - train_model_CL1.py
    - train_model_CL2.py
    - train_model_CL3.py
    - train_model_CL1_ERA_interp.py
    - train_model_CL2_ERA_interp.py
    - train_model_CL3_ERA_interp.py

7) Once models are made, or using the current models, raster_predictions.py/raster_predictions_ERA_interp.py/raster_predictions_no_subsampling can be used to make predictions for all of the complete (total) files.

