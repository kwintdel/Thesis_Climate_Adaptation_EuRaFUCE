# raster 1km
Information about how this directory is organised and in what order certain code should be run.
Information about dependencies can be found in the subdirectory 'jobs', where the necessary modules for each code file are defined.
This directory contains files to make the data for 653 new cities to make predictions with Eu-RaFUCE1km mode and perc.
Make sure to adjust the file paths accordingly, the code is not made fully optimal to use outside of the Ghent University Tier 2 infrastructure.
The data for the bounding boxes is present in the subdirectory 'data'.

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

4) All separate rasters can be combined into .csv files using raster_total.py or raster_total_corine_perc.py for Eu-RaFUCE1km perc.

Take note that no code is provided to calculate the statistics per city, necessary to divide the cities into clusters. This can however be done by changing the corresponding code from raster_100m slightly. 
Further, also the raster_total_corine_perc.py does not use the interpolated ERA values yet, so do change this according to the code from raster_100m if you want to use it.

