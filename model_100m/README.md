# model 100m
Information about how this directory is organised and in what order certain code should be run.
Information about dependencies can be found in the subdirectory 'jobs', where the necessary modules for each code file are defined.
This directory contains files to make the data used to train and evaluate Eu-RaFUCE.
Make sure to adjust the file paths accordingly, the code is not made fully optimal to use outside of the Ghent University Tier 2 infrastructure.
The models made during the thesis 'Spatiotemporal modelling of air temperature over European cities using machine learning' can be found in the subdirectory 'models'.

1) the makeraster.py should be run to generate the 100m resolution rasters

2) The following list of python files can all be run at the same time and are needed to calculate separate grids for eacht city for this variable:
    - raster_coast.py
    - raster_CORINE.py
    - raster_elev_DMET.py
    - raster_ERA_RH_sep.py
    - raster_ERA_solar_sep.py
    - raster_height.py
    - raster_imperv.py
    - raster_population.py
    - raster_geopotential.py

3) Now the Rh and other ERA values can be made into a file per city (previously multiple files were made per month for each city, you can also use those files if you want to only use one month of data for predictions):
    - raster_ERA_RH_percity.py
    - raster_ERA_solar_percity.py

4) All separate rasters can be combined into .csv files using raster_total.py

5) Once models are made, or using the current models, raster_predictions.py can be used to make predictions for all of the complete (total) files.
