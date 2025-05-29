#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=3:00:00
#PBS -l mem=100gb
module purge 

module load xarray/2023.9.0-gfbf-2023a
module load scikit-learn/1.3.1-gfbf-2023a
module load Python-bundle-PyPI/2024.06-GCCcore-13.3.0

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_scripts
python3 ./clustering.py