#!/bin/bash
#Do production runs

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --gpus-per-node=4
#SBATCH --time=12:00:00

module load parallel
module load conda/Mambaforge-23.1.0-1

mamba activate hoomd

nseed=$1

#phis=(0.1 0.4 0.7)
phis=(0.1 0.4)
#Ls=(50.0 100.0 200.0 400.0)
Ls=(200.0)
taus=(0.1 1.0 10.0 inf)
Lambdas=(1.0 3.0 10.0 30.0)
vas=(1.0)
seeds=($(seq 1 $nseed))

srun --no-kill --wait=0 parallel -k --jobs 4 python $HOME/active-assembly-hoomd/scripts/run.py --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]} ::: --tau ::: ${taus[@]} ::: --lambda ::: ${Lambdas[@]} ::: --va ::: ${vas[@]}
