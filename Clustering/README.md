# Clustering
Information about how this directory is organised and in what order certain code should be run.
Information about dependencies can be found in the subdirectory 'jobs', where the necessary modules for each code file are defined. 
The subdirectory 'data' contains the data used to make the knn classifier as well as the scaling data.
The subdirectory 'classifier' contains the scaling as well as the knn classifier.
This directory contains files used to make the clustering knn classifiers as well as code to evaluate to which cluster a new city belongs. 
Make sure to adjust the file paths accordingly, the code is not made fully optimal to use outside of the Ghent University Tier 2 infrastructure.

1) At first some necessary characteristics for all cities can be made with all_city_char.py.

2) The correct characteristics can be extracted with average_precip_temp_train.py, possibly some characteristics will still be needed and some extra code is needed.

3) To make the knn classifiers stored in 'classifier', you have to execute train_clustering_total.py to obtain characteristics from all of the 100 cities used to build and evaluate Eu-RaFUCE. The results obtained in the thesis are available in 'data'. If you only want to classify new cities based on the supplemented classifiers, go to step 6.

4) To make the knn classifiers, execute make_knn_classifier.py.

5) To test these classifiers, run clustering_test.py, which clusters the 100 cities used to evaluate Eu-RaFUCE. The outcomes from this testing can be visualised using test_cluster_outcomes.ipynb.

6) To combine all characteristics for some new cities you want to cluster, execute new_clustering_total.py and then run clustering.py.

