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
potential=$7
compressibility=$8
kT=$9

minseed=1
seeds=($(seq 1 $nseed))

seedbyfour="$(($nseed / 4))"
if (( $(echo "$seedbyfour==0" | bc -l) )); then
    echo "running 1 seed"
    seedbyfour=1
fi

seedints=($(seq 0 "$(($seedbyfour))"))

grid_size=128

#default time parameters for va=1
dt=0.00025
trun=250
tfreq=1.0

if (($(echo "$potential" = "none" | bc -l) )); then
    echo "setting timestep to 0.01"
    dt=0.01
fi

if (( $(echo "$va==2.0" |bc -l) )); then
    dt=0.00005
    trun=125
    tfreq=0.5
fi
if (( $(echo "$va==0.5" |bc -l) )); then
    dt=0.0002
    trun=500
    tfreq=2.0
fi
if (( $(echo "$va==0.1" |bc -l) )); then
    dt=0.001
    trun=2500
    tfreq=10.0
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
                srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run.py -d 3 -f $tfreq -t $trun -o $outfolder -dt $dt --phi $phi -L $L -g $grid_size --seed $seed --tau $tau --va $va --lambda $Lambda --kT $kT --potential $potential --compressibility $compressibility > $SCRATCH/active-assembly-hoomd/log/run_3d_manyseed_${compressibility}_phi=${phi}_L=${L}_va=${va}_tau=${tau}_lambda=${Lambda}_seed=${seed}.out &
            fi
        fi
    done
    wait
done
wait