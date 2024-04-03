#!/bin/bash
#Do production runs

#SBATCH -A m4494
#SBATCH --qos=debug
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --ntasks-per-node=4
##SBATCH --gpus-per-task=1
#SBATCH --time=0:30:00
##SBATCH -c 32
##SBATCH --mem-per-gpu=55G

module load parallel
module load conda/Mambaforge-23.1.0-1

mamba activate hoomd

nseed=$1

#phis=(0.1 0.4 0.7)
#phis=(0.1 0.4)
phis=(0.4)
#Ls=(50.0 100.0 200.0 400.0)
Ls=(200.0)
#taus=(0.1 1.0 10.0 inf)
taus=(10.0)
Lambdas=(1.0 3.0 10.0 30.0)
vas=(1.0)
seeds=($(seq 1 $nseed))

interp="none"

if [ ! -d $SCRATCH/active-assembly-hoomd/log ]; then
    mkdir $SCRATCH/active-assembly-hoomd/log;
fi

#srun --no-kill --wait=0 parallel -k --jobs 40 python $HOME/active-assembly-hoomd/scripts/run.py --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]} ::: --tau ::: ${taus[@]} ::: --lambda ::: ${Lambdas[@]} ::: --va ::: ${vas[@]}
srun --exact -u -n 1 --gpus-per-task 1 -c 1 --mem-per-gpu=8G python $HOME/active-assembly-hoomd/scripts/run.py --phi 0.1 -L 200.0 --seed 1 --tau 0.1 --va 1.0 --lambda 1.0 -t 10.0  > $SCRATCH/active-assembly-hoomd/log/run_l=1.out &
srun --exact -u -n 1 --gpus-per-task 1 -c 1 --mem-per-gpu=8G python $HOME/active-assembly-hoomd/scripts/run.py --phi 0.1 -L 200.0 --seed 1 --tau 0.1 --va 1.0 --lambda 3.0 -t 10.0 > $SCRATCH/active-assembly-hoomd/log/run_l=3.out &
srun --exact -u -n 1 --gpus-per-task 1 -c 1 --mem-per-gpu=8G python $HOME/active-assembly-hoomd/scripts/run.py --phi 0.1 -L 200.0 --seed 1 --tau 0.1 --va 1.0 --lambda 10.0 -t 10.0 > $SCRATCH/active-assembly-hoomd/log/run_l=10.out &
srun --exact -u -n 1 --gpus-per-task 1 -c 1 --mem-per-gpu=8G python $HOME/active-assembly-hoomd/scripts/run.py --phi 0.1 -L 200.0 --seed 1 --tau 0.1 --va 1.0 --lambda 30.0 -t 10.0 > $SCRATCH/active-assembly-hoomd/log/run_l=30.out &

#srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G parallel -k --lb --jobs 4 "python $HOME/active-assembly-hoomd/scripts/run.py --phi {1} -L {2} --va {3} --tau {4} --lambda {5} --seed {6} -t 10.0 > $SCRATCH/active-assembly-hoomd/log/run_phi={1}_L={2}_va={3}_tau={4}_lambda={5}_seed={6}.out" \
#                       ::: ${phis[@]} \
#                      ::: ${Ls[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${Lambdas[@]} \
#                        ::: ${seeds[@]}

#wait