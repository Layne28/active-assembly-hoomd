#!/bin/bash
#Check if trajectories in directories are full-length,
#otherwise rerun them with a smaller time step

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --ntasks-per-node=4
#SBATCH --time=24:00:00

module load parallel
module load conda/Mambaforge-23.1.0-1

mamba activate hoomd

nseed=$1
phi=$2
L=$3
tau=$4
va=$5

#phis=(0.1 0.4 0.7)
phis=(0.1 0.4)
#Ls=(50.0 100.0 200.0 400.0)
Ls=(200.0)
taus=(0.1 1.0 10.0 "inf")
Lambdas=(1.0 3.0 10.0 30.0)
vas=(1.0)
seeds=($(seq 1 $nseed))

potential="wca"
interp="linear"
compressibility="compressible"
cov_type="exponential"
d=2
dt=0.0001

#srun --no-kill --wait=0 parallel -k --jobs 40 python $HOME/active-assembly-hoomd/scripts/run.py --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]} ::: --tau ::: ${taus[@]} ::: --lambda ::: ${Lambdas[@]} ::: --va ::: ${vas[@]}
for seed in "${seeds[@]}"; do
    echo "seed $seed"
    for Lambda in "${Lambdas[@]}"; do
        filename=$SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT=${kT}/phi=${phi}/va=${va}/tau=${tau}/lambda=${Lambda}/Lx=${L}_Ly=${L}/nx=400_ny=400/interpolation=${interp}/${compressibility}/${cov_type}/seed=${seed}/prod/traj.gsd
        if [ "$tau" -eq "inf" ]; then
            filename=$SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT=${kT}/phi=${phi}/va=${va}/quenched/lambda=${Lambda}/Lx=${L}_Ly=${L}/nx=400_ny=400/interpolation=${interp}/${compressibility}/${cov_type}/seed=${seed}/prod/traj.gsd
        if python $HOME/active-assembly/hoomd/scripts/check_complete.py $filename; then
            echo "Trajectory complete. Skipping..."
        else
            echo "Rerunning trajectory: $filename"
            srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run.py --dt $dt --phi $phi -L $L --seed $seed --tau $tau --va $va --lambda $Lambda > $SCRATCH/active-assembly-hoomd/log/run_phi=${phi}_L=${L}_va=${va}_tau=${tau}_lambda=${Lambda}_seed=${seed}.out &
    done
    wait
    #sleep 10s
done