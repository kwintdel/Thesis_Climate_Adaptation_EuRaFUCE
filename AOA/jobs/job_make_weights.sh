#!/bin/bash
#PBS -l nodes=1:ppn=5
#PBS -l walltime=00:01:00
#PBS -l mem=200mb
module purge 

module load scikit-learn/1.0.1-foss-2021b
#module load Python-bundle-PyPI/2023.06-GCCcore-12.3.0
module load SciPy-bundle/2021.10-foss-2021b


cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_scripts
python3 ./make_weights.py