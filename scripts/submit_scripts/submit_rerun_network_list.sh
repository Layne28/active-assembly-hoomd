#!/bin/bash
#Read in trajectories to be rerun from file

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --ntasks-per-node=4
#SBATCH --time=24:00:00

module load parallel
module load conda/Mambaforge-23.1.0-1

mamba activate hoomd

myfile=$1
dt=0.00005
trun=250
tfreq=1.0
grid_size=200
potential="fene"

outfolder=$SCRATCH/active-assembly-hoomd/manyseed

ncurr=0
while read line; do 
    
    #Let only four trajectories run at once
    echo "Running $line"
    
    #printf %s\\n "${patharr[@]}"

    ncurr=$((ncurr+1))
    echo $ncurr
    if (( $ncurr == 5 )); then
        wait
        ncurr=0
    fi

    #Extract parameters from filename
    Nx=96
    Ny=112
    seed=1
    tau=1.0
    va=1.0
    Lambda=1.0
    IFS=/ read -r -a patharr <<<"$line"
    for elem in "${patharr[@]}"; do
       if [[ $elem == phi* ]]; then
           phi="${elem#*=}"
           #echo $phi
       fi 
       if [[ $elem == Nx* ]]; then
           N="${elem#*=}"
           Nx="${N%%_*}"
           Ny="${N#*_}"
           Ny="${Ny#*=}"
           #echo $Nx
           #echo $Ny
           if (( $(echo "$Nx==96" |bc -l) )); then
               grid_size=200
           fi
           #echo $L
       fi 
       if [[ $elem == seed* ]]; then
           seed="${elem#*=}"
           #echo $seed
       fi 
       if [[ $elem == tau* ]]; then
           tau="${elem#*=}"
           #echo $tau
       fi 
       if [[ $elem == quenched ]]; then
           tau="inf"
           #echo $tau
       fi 
       if [[ $elem == va* ]]; then
           va="${elem#*=}"
           #echo $va
       fi 
       if [[ $elem == lambda* ]]; then
           Lambda="${elem#*=}"
           #echo $Lambda
       fi 
    done
    
    #Run trajectory
    srun --exact -u -n 1 --gpus-per-task 1 -c 32 --mem-per-gpu=55G python $HOME/active-assembly-hoomd/scripts/run_network.py -f $tfreq -t $trun -o $outfolder --dt $dt -Nx $Nx -Ny $Ny -gx $grid_size -gy $grid_size --seed $seed --tau $tau --va $va --lambda $Lambda -p $potential > $SCRATCH/active-assembly-hoomd/log/rerun_Nx=${Nx}_Ny=${Ny}_va=${va}_tau=${tau}_lambda=${Lambda}_seed=${seed}.out &

done <$myfile
wait