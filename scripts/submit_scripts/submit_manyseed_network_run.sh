#!/bin/bash
#Do production runs for network

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
Nx=$2
Ny=$3
tau=$4
va=$5
Lambda=$6
potential=$7

seeds=($(seq 1 $nseed))


seedbyfour="$(($nseed / 4))"
seedints=($(seq 0 "$(($seedbyfour-1))"))

grid_size=400
if (( $(echo "$Nx==96" |bc -l) )); then
    grid_size=200
fi
echo $grid_size
dt=0.00005 #0.01

outfolder=$SCRATCH/active-assembly-hoomd/manyseed

#Run four seeds at a time
for seedint in "${seedints[@]}"; do
    nums=($(seq 1 4))
    for num in "${nums[@]}"; do
        seed="$(($(($seedint * 4)) + $num))"
        echo "seed $seed"
        srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run_network.py -f 1.0 -t 250 -o $outfolder -dt $dt -Nx $Nx -Ny $Ny -gx $grid_size -gy $grid_size --seed $seed --tau $tau --va $va --lambda $Lambda -p $potential > $SCRATCH/active-assembly-hoomd/log/run_network_manyseed_Nx=${Nx}_Ny=${Ny}_va=${va}_tau=${tau}_lambda=${Lambda}_seed=${seed}.out &
    done
    wait
done