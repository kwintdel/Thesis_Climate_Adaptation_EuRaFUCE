#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=6:00:00
#PBS -l mem=300gb
module purge 

module load dask/2023.12.1-foss-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/model_scripts
python3 ./train_val_cities.py