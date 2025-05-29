#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=5:00:00
#PBS -l mem=400gb
module purge 

module load rasterio/1.3.9-foss-2023a
module load rioxarray/0.15.0-foss-2023a
module load xarray/2023.9.0-gfbf-2023a
module load matplotlib/3.7.2-gfbf-2023a
module load netcdf4-python/1.6.4-foss-2023a
module load dask/2023.12.1-foss-2023a
module load FFmpeg/6.0-GCCcore-12.3.0
module load geocube/0.4.3-foss-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/raster_1km_scripts
python3 ./raster_CORINE.py