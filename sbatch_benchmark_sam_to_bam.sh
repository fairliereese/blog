#!/bin/sh
#SBATCH -A SEYEDAM_LAB
#SBATCH --output=peeps.out
#SBATCH --error=peeps.err
#SBATCH --time=06:00:00
#SBATCH -J peeps
#SBATCH --mail-type=START,END
#SBATCH --partition=standard
#SBATCH --cpus-per-task=16

python sam_to_bam.py