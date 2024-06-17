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
L=$2
tau=$3
va=$4
Lambda=$5

minseed=1
seeds=($(seq 1 $nseed))

seedbyfour="$(($nseed / 4))"
seedints=($(seq 0 "$(($seedbyfour))"))

grid_size=400
if (( $(echo "$L==100.0" |bc -l) )); then
    grid_size=200
fi

#default time parameters for va=1
dt=0.01
trun=2000
tfreq=0.25

if (($(echo "$potential" = "none" | bc -l) )); then
    echo "setting timestep to 0.01"
    dt=0.01
fi

if (( $(echo "$va==2.0" |bc -l) )); then
    dt=0.005
    trun=1000
    tfreq=0.125
fi
if (( $(echo "$va==0.5" |bc -l) )); then
    dt=0.02
    trun=4000
    tfreq=0.5
fi
if (( $(echo "$va==0.1" |bc -l) )); then
    dt=0.1
    trun=20000
    tfreq=2.5
fi

outfolder=$SCRATCH/active-assembly-hoomd/manyseed

#Run four seeds at a time
for seedint in "${seedints[@]}"; do
    nums=($(seq 1 4))
    for num in "${nums[@]}"; do
        seed="$(($(($seedint * 4)) + $num))"
        if [ $seed -le $nseed ]; then
            if [ $seed -ge $minseed ]; then
                echo "seed $seed"
                srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run_single_particle.py -f $tfreq -t $trun -o $outfolder -dt $dt -L $L -g $grid_size --seed $seed --tau $tau --va $va --lambda $Lambda > $SCRATCH/active-assembly-hoomd/log/run_single_particle_manyseed_L=${L}_va=${va}_tau=${tau}_lambda=${Lambda}_seed=${seed}.out &
            fi
        fi
    done
    wait
done
wait