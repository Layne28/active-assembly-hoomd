#!/bin/bash
#Do production runs

#SBATCH --account=esx-delta-gpu
#SBATCH --partition=gpuA100x4
#SBATCH --nodes=1
#SBATCH --gpu-bind=closest
#SBATCH --gpus-per-node=4
#SBATCH --exclusive
#SBATCH --mem=208G
#SBATCH --time=12:00:00

module load parallel/20220522
source ~/.bash_profile
source activate hoomd

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
