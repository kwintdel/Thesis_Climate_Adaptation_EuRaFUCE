#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=10:00:00
#PBS -l mem=100gb
module purge 

module load dask/2023.12.1-foss-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_scripts
python3 ./AOA_train_val_folds.py