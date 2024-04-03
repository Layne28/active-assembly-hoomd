#!/bin/bash
#Do production runs

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --ntasks-per-node=4
#SBATCH --time=1:00:00

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

interp="none"

#srun --no-kill --wait=0 parallel -k --jobs 40 python $HOME/active-assembly-hoomd/scripts/run.py --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]} ::: --tau ::: ${taus[@]} ::: --lambda ::: ${Lambdas[@]} ::: --va ::: ${vas[@]}
srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run.py --phi 0.1 -L 200.0 --seed 1 --tau 10.0 --va 1.0 --lambda 1.0 -t 10.0 &
srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run.py --phi 0.1 -L 200.0 --seed 1 --tau 10.0 --va 1.0 --lambda 3.0 -t 10.0 &
srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run.py --phi 0.1 -L 200.0 --seed 1 --tau 10.0 --va 1.0 --lambda 10.0 -t 10.0 &
srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run.py --phi 0.1 -L 200.0 --seed 1 --tau 10.0 --va 1.0 --lambda 30.0 -t 10.0 &

wait