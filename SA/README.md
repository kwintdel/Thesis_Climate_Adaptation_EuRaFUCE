# Sensitivity analysis (SA)
Information about how this directory is organised and in what order certain code should be run.

This directory contains information about how the DI thresholds for the AOA were made for the Eu-RaFUCE model, so that it can be easily adapted for other models, as well as code which shows how to evaluate the AOA for new data.


1) Before running the sensitivity analysis, we need to add one more variable if we want to investigate the effect from specific humidity instead of relative humidity. with:
    - specific_humidity.ipynb

## General sensitivity analysis
To make the figures from the sensitivity analysis as in the thesis, play with the cells in the following code. The first cells in each notebook make the DDSI's for each feature for every cluster. Once these are made, one can play with the code to get interesting figures:
    - Sensitivity_Analysis_CL1.ipynb
    - Sensitivity_Analysis_CL2.ipynb
    - Sensitivity_Analysis_CL3.ipynb

## Case studies
All code to make the figures of the case studies in the thesis is given in case_studies.ipynb. To also add the black pixels of the AOA, combine this notebook with AOA_Cl2.ipynb in the AOA directory.



