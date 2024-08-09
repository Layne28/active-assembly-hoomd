#!/bin/bash
#Do production runs

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --ntasks-per-node=1
#SBATCH --time=4:00:00

module load parallel
module load conda/Mambaforge-23.1.0-1

mamba activate hoomd

seed=$1
phi=$2
L=$3
tau=$4
va=$5
Lambda=$6
potential=$7
compressibility=$8
kT=$9

interp="linear"

srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run.py -t 250 --phi $phi -L $L --seed $seed --tau $tau --va $va --lambda $Lambda --kT $kT --potential $potential --compressibility $compressibility > $SCRATCH/active-assembly-hoomd/log/run_phi=${phi}_L=${L}_va=${va}_tau=${tau}_lambda=${Lambda}_seed=${seed}.out &
wait