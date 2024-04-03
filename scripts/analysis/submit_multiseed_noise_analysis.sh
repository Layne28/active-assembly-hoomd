#!/bin/bash
#Submit analysis of active noise simulation

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=12:00:00

myfolder=$1
nseed=$2

echo "Running analysis of data in folder: $myfolder"
module load parallel
module load conda/Mambaforge-23.1.0-1
mamba activate hoomd

run_dir=${HOME}/AnalysisTools/AnalysisTools/
echo ${run_dir}

#Do per-trajectory analysis first
for (( i=1; i<=$nseed; i++ ))
do
    echo "Running seed: $i"
    python $run_dir/noise_stats.py $myfolder/seed=$i/prod/noise_traj.h5
done

srun parallel -k --jobs 128 python $HOME/active-assembly-hoomd/scripts/randomize.py --init_style ::: $init_style ::: --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]}

#Now do analysis over all trajectories
#python ${run_dir}/trajectory_stats.py ${myfolder} noise_stats average postprocessed
#python ${run_dir}/trajectory_stats.py ${myfolder} noise histogram noise
python ${run_dir}/trajectory_stats.py ${myfolder} noise average noise