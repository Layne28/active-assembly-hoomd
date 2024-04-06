#!/bin/bash
#Submit analysis of active noise simulation

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=12:00:00

tmax=100.000000

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
    python $run_dir/energy.py $myfolder/seed=$i/prod/traj.gsd
    #python $run_dir/msd.py $myfolder/seed=$i/prod/traj.h5 5 $tmax
    python $run_dir/structure_factor.py $myfolder/seed=$i/prod/traj.gsd 5
    python $run_dir/cluster.py $myfolder/seed=$i/prod/traj.gsd
done

#Now do analysis over all trajectories
python ${run_dir}/trajectory_stats.py ${myfolder} "energies_and_forces" average postprocessed
#python ${run_dir}/trajectory_stats.py ${myfolder} msd average postprocessed
python ${run_dir}/trajectory_stats.py ${myfolder} sq average postprocessed
python ${run_dir}/trajectory_stats.py ${myfolder} sq_traj average postprocessed
python ${run_dir}/trajectory_stats.py ${myfolder} csd csd postprocessed
#python ${run_dir}/trajectory_stats.py ${myfolder} vel histogram particle
#python ${run_dir}/trajectory_stats.py ${myfolder} vel average particle