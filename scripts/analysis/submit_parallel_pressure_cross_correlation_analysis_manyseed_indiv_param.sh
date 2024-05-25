#!/bin/bash
#Submit analysis of density and noise cross-correlation

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=12:00:00

njob=64
nseed=50

potential="fene"
interp="linear"
compressibility="compressible"
cov_type="exponential"
d=2
Nx=96
Ny=112
nx=200

tau=$1
lambda=$2

kT=0.000000
va=1.000000
seeds=($(seq 1 $nseed))

mydir=$SCRATCH

module load parallel
module load conda/Mambaforge-23.1.0-1
mamba activate hoomd

run_dir=${HOME}/AnalysisTools/AnalysisTools/
echo ${run_dir}

#Do per-trajectory analysis first
echo "Doing cross-correlation analysis..."
srun parallel -k --lb --jobs $njob "python $run_dir/field_particle_correlation.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT=${kT}/va=${va}/${tau}/lambda=${lambda}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={1}/prod/traj.gsd pressure > $SCRATCH/active-assembly-hoomd/log/pressure_cross_corr_kT=${kT}_va=${va}_${tau}_lambda=${lambda}_seed={1}.out" \
                        ::: ${seeds[@]} &

wait   

#Now do analysis over all trajectories
echo "Averaging pressure cross-correlation..."
python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT=${kT}/va=${va}/${tau}/lambda=${lambda}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ 'pressure_noise_correlation' average postprocessed > $SCRATCH/active-assembly-hoomd/log/pressure_noise_corr_avg_kT=${kT}_va=${va}_${tau}_lambda=${lambda}_avg.out

python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT=${kT}/va=${va}/${tau}/lambda=${lambda}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ 'pressure_noise_correlation_spatial' average postprocessed > $SCRATCH/active-assembly-hoomd/log/pressure_noise_corr_spatial_avg_kT=${kT}_va=${va}_${tau}_lambda=${lambda}_avg.out

