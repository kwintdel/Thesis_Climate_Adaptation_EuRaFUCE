#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=2:00:00
#PBS -l mem=50gb
module purge 

module load dask/2023.12.1-foss-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_scripts
python3 ./assign_to_cluster.py