# raster 100m
Information about how this directory is organised and in what order certain code should be run.
Information about dependencies can be found in the subdirectory 'jobs', where the necessary modules for each code file are defined.
This directory contains files to make the data for 653 new cities to make predictions with Eu-RaFUCE.
Make sure to adjust the file paths accordingly, the code is not made fully optimal to use outside of the Ghent University Tier 2 infrastructure.
The data for the bounding boxes is present in the subdirectory 'data'.

1) the makeraster.py should be run to generate the 100m resolution rasters

2) The following list of python files can all be run at the same time and are needed to calculate the statistics:
    - raster_coast.py
    - raster_CORINE.py
    - raster_elevation.py
    - raster_ERA_RH.py
    - raster_ERA2.py
    - raster_height.py
    - raster_imperv.py
    - raster_population.py
    - raster_solar.py

3) Now both city_stats.py and CORINE_stats.py can be run to calculate extent statistics with the previous data. These statistics can be used to cluster the cities and give some general further information.

4) The following python files need to be run to get a raster of the temporal data:
    - raster_ERA_RH_date.py
    - raster_ERA_solar_date.py

5) Now the complete data can be made with raster_total.py

5) Using Eu-RaFUCE, raster_predictions.py can be used to make predictions for all of the complete (total) files.