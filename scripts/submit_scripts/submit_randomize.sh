#!/bin/bash
#Randomize initial lattice configuration

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=12:00:00

module load parallel
module load conda/Mambaforge-23.1.0-1

mamba activate hoomd

nseed=$1
init_style="uniform"

phis=(0.1 0.4 0.7)
Ls=(50.0 100.0 200.0 400.0)
seeds=($(seq 1 $nseed))

srun parallel -k --jobs 128 python $HOME/active-assembly-hoomd/scripts/randomize.py --init_style ::: $init_style ::: --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]}
