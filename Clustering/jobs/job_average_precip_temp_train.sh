#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=5:00:00
#PBS -l mem=300gb

module load xarray/2023.9.0-gfbf-2023a
module load dask/2023.12.1-foss-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_scripts
python3 ./average_precip_temp_train.py