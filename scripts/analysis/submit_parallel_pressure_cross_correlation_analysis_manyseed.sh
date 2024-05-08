#!/bin/bash
#Submit analysis of density and noise cross-correlation

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=2:00:00

njob=32
nseed=50

potential="fene"
interp="linear"
compressibility="compressible"
cov_type="exponential"
d=2
Nx=96
Ny=112
nx=200

kTs=(0.000000)
vas=(1.000000)
#vas=($1)
taus=("tau=0.100000" "tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
#lambdas=(1.000000 3.000000 10.000000 30.000000)
lambdas=(1.000000 3.000000 5.000000 10.000000)
seeds=($(seq 1 $nseed))

mydir=$SCRATCH

module load parallel
module load conda/Mambaforge-23.1.0-1
mamba activate hoomd

run_dir=${HOME}/AnalysisTools/AnalysisTools/
echo ${run_dir}

#Do per-trajectory analysis first
echo "Doing cross-correlation analysis..."
srun parallel -k --lb --jobs $njob "python $run_dir/field_particle_correlation.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd $SCRATCH/active-assembly-hoomd/manyseed/noise/${d}d/{3}/lambda={4}/nx=${nx}_ny=${nx}/${compressibility}/${cov_type}/seed={5}/noise_traj.h5 pressure > $SCRATCH/active-assembly-hoomd/log/pressure_cross_corr_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\' &

wait   

#Now do analysis over all trajectories
echo "Averaging pressure cross-correlation..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ 'pressure_noise_correlation' average postprocessed > $SCRATCH/active-assembly-hoomd/log/pressure_noise_corr_avg_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait
