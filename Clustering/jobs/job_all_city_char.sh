#!/bin/bash
#PBS -l nodes=2:ppn=10
#PBS -l walltime=15:00:00
#PBS -l mem=400gb

module load xarray/2023.9.0-gfbf-2023a
module load dask/2023.12.1-foss-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_scripts
python3 ./all_city_char.py