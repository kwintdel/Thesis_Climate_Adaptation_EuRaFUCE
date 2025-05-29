# Thesis: Effect of climate adaptation measures in European cities according to the Eu-RaFUCE model

information about what directories contain what information:

* model_100m: this contains all the files necessary to create the 100m resolution data for the cities used to train and evaluate Eu-RaFUCE.

* model_1km: this contains all the files necessary to create the 1km resolution data for the cities used to train and evaluate Eu-RaFUCE1km perc and Eu-RaFUCE1km mode.

* raster_100m: this contains all the files to create 100m resolution rasters of 653 European cities based solemnly on a min_lon, min_lat, max_lon, max_lat square. Further it contains the scripts to cut out these rasters from larger rasters to obtain all of the variables needed for the model. This both to first refer every city to a cluster of the model and then to create the necessary data to calculate the Area Of Application (AOA) and apply the model.

* raster_1km: this contains the same steps as raster_100m, but now for a 1km resolution instead of a 100m.

*  Clustering: this contains all of the files to be able to remake the knn classifier for the cluster assignment as well as code to assign a new city to a cluster of Eu-RaFUCE.

* AOA: this contains all files to be able to remake the thresholds to evaluate the AOA as well as code to evaluate new cities based on the thresholds obtained during the thesis.

* SA: this contains all files to calculate the DDSI's for the training, validation and test data of Eu-RaFUCE as well as notebooks to make the figures from the thesis.
