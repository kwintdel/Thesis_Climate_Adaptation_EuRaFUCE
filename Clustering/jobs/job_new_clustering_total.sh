#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=1:00:00
#PBS -l mem=100gb
module purge 

module load xarray/2023.9.0-gfbf-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_scripts
python3 ./new_clustering_total.py