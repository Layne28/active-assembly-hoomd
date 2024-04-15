#!/bin/bash
#Do production runs

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
Lambda=$6

#phis=(0.1 0.4 0.7)
phis=(0.1 0.4)
#Ls=(50.0 100.0 200.0 400.0)
Ls=(200.0)
taus=(0.1 1.0 10.0 inf)
Lambdas=(1.0 3.0 10.0 30.0)
vas=(1.0)
seeds=($(seq 1 $nseed))

seedbyfour="$(($nseed / 4))"
seedints=($(seq 0 "$(($seedbyfour-1))"))

outfolder=$SCRATCH/active-assembly-hoomd/manyseed

#Run four seeds at a time
for seedint in "${seedints[@]}"; do
    nums=($(seq 1 4))
    for num in "${nums[@]}"; do
        seed="$(($(($seedint * 4)) + $num))"
        echo "seed $seed"
        srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run.py -f 1.0 -o $outfolder -dt 0.0002 --phi $phi -L $L --seed $seed --tau $tau --va $va --lambda $Lambda > $SCRATCH/active-assembly-hoomd/log/run_manyseed_phi=${phi}_L=${L}_va=${va}_tau=${tau}_lambda=${Lambda}_seed=${seed}.out &
    #wait
    #sleep 10s
    done
    #echo "wait"
    wait
done