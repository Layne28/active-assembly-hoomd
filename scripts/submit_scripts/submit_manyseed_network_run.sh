#!/bin/bash
#Do production runs for network

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --ntasks-per-node=4
#SBATCH --time=48:00:00

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
startseed=$8 #should set default to zero

seeds=($(seq $startseed $nseed))
seedbyfour="$(($nseed / 4))"
startbyfour="$(($startseed / 4))"
seedints=($(seq $startbyfour "$(($seedbyfour-1))"))

grid_size=400
if (( $(echo "$Nx==96" |bc -l) )); then
    grid_size=200
fi
echo $grid_size
dt=0.00001 #0.01

if (( $(echo "$va==1.00" |bc -l) )); then
    dt=0.000003
    trun=250
    tfreq=1.0
fi

if (( $(echo "$va==0.30" |bc -l) )); then
    dt=0.000005
    if (( $(echo "$tau==10.0" |bc -l) )); then
        dt=0.00001
    fi
    if (( $(echo "$tau==1.0" |bc -l) )); then
        dt=0.00001
    fi
    if (( $(echo "$tau==0.1" |bc -l) )); then
        dt=0.00001
    fi
    trun=250 #833.333333
    tfreq=1.0 #3.33333
fi

if (( $(echo "$va==0.10" |bc -l) )); then
    dt=0.000033
    trun=250 #2500
    tfreq=1.0 #10.0
fi

if (( $(echo "$va==0.03" |bc -l) )); then
    dt=0.0001
    trun=250 #8333.333333
    tfreq=1.0 #33.333333
fi

if (( $(echo "$va==0.01" |bc -l) )); then
    dt=0.000333
    trun=250 #25000
    tfreq=1.0 #100.0
fi

outfolder=$SCRATCH/active-assembly-hoomd/manyseed

#Run four seeds at a time
for seedint in "${seedints[@]}"; do
    nums=($(seq 1 4))
    for num in "${nums[@]}"; do
        seed="$(($(($seedint * 4)) + $num))"
        echo "seed $seed"
        srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run_network.py -f $tfreq -t $trun -o $outfolder -dt $dt -Nx $Nx -Ny $Ny -gx $grid_size -gy $grid_size --seed $seed --tau $tau --va $va --lambda $Lambda -p $potential > $SCRATCH/active-assembly-hoomd/log/run_network_manyseed_Nx=${Nx}_Ny=${Ny}_va=${va}_tau=${tau}_lambda=${Lambda}_seed=${seed}.out &
    done
    wait
done
wait