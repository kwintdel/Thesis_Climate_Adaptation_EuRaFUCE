#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=1:00:00
#PBS -l mem=100gb
module purge 

module load R-bundle-CRAN/2023.12-foss-2023a
module load R/4.3.2-gfbf-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_scripts
Rscript ./make_DI3_parallel_test.R