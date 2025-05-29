#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=4:00:00
#PBS -l mem=300gb
module purge 

module load xarray/2023.9.0-gfbf-2023a
module load netcdf4-python/1.6.4-foss-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/model_scripts
python3 ./raster_ERA_RH_interp_percity.py