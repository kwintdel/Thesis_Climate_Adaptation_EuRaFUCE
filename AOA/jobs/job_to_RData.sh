#!/bin/bash
#PBS -l nodes=1:ppn=16
#PBS -l walltime=6:00:00
#PBS -l mem=100gb
module purge 

module load R/4.3.2-gfbf-2023a

cd /data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_scripts
Rscript ./to_Rdata.R