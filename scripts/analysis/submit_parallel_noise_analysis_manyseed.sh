#!/bin/bash
#Submit analysis of active noise simulation

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=1:00:00

njob=32

nseed=50

compressibility="compressible"
cov_type="exponential"
d=2
nx=400

taus=("tau=0.100000" "tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
lambdas=(1.000000 3.000000 5.000000 10.000000 20.000000)
seeds=($(seq 1 $nseed))

module load parallel
module load conda/Mambaforge-23.1.0-1
mamba activate hoomd

run_dir=${HOME}/AnalysisTools/AnalysisTools/
echo ${run_dir}

#Do per-trajectory analysis first
echo "Getting per-trajectory correlations..."
#srun parallel -k --lb --jobs $njob "python $run_dir/noise_stats.py $SCRATCH/active-assembly-hoomd/manyseed/noise/${d}d/{1}/lambda={2}/nx=${nx}_ny=${nx}/${compressibility}/${cov_type}/seed={3}/noise_traj.h5  > $SCRATCH/active-assembly-hoomd/log/noise_analysis_{1}_lambda={2}_seed={3}.out" \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]} \
#                        ::: ${seeds[@]} | tr -d \''"\' &
#wait

#Now do analysis over all trajectories
echo "Averaging noise correlations..."
srun parallel -k --lb --jobs $njob "python ${run_dir}/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/noise/${d}d/{1}/lambda={2}/nx=${nx}_ny=${nx}/${compressibility}/${cov_type}/ noise_stats average postprocessed --subfolder '' --max_num_traj ${nseed} > $SCRATCH/active-assembly-hoomd/log/noise_analysis_{1}_lambda={2}_avg.out" \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} | tr -d \''"\' &
wait