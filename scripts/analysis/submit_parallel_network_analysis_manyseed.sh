#!/bin/bash
#Submit analysis of active noise simulation

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=12:00:00

njob=64

tmax=100.000000
nseed=20

potential="fene"
interp="linear"
compressibility="compressible"
cov_type="exponential"
d=2
Nx=96
Ny=112
nx=200

kTs=(0.000000)
vas=(0.010000 0.030000 0.100000 0.300000) # 1.000000)
taus=("tau=0.100000" "tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
lambdas=(1.000000 3.000000 5.000000 10.000000 20.000000)
seeds=($(seq 1 $nseed))

mydir=$SCRATCH

module load parallel
module load conda/Mambaforge-23.1.0-1
mamba activate hoomd

run_dir=${HOME}/AnalysisTools/AnalysisTools/
echo ${run_dir}

#Do per-trajectory analysis first

echo "Getting strain histograms..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ strain histogram particle > $SCRATCH/active-assembly-hoomd/log/strain_histo_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait

echo "Getting stress histograms..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ stress histogram particle > $SCRATCH/active-assembly-hoomd/log/stress_histo_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait


#echo "Getting stress and strain time correlations..."
#srun parallel -k --lb --jobs $njob "python $run_dir/correlation.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --nlast 3 --quantity strain --corrtype time > $SCRATCH/active-assembly-hoomd/log/strain_time_corr_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]} \
#                        ::: ${seeds[@]} | tr -d \''"\' &
#wait  

#srun parallel -k --lb --jobs $njob "python $run_dir/correlation.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --nlast 3 --quantity strain --corrtype space --rmax 15.0 > $SCRATCH/active-assembly-hoomd/log/strain_spatial_corr_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]} \
#                        ::: ${seeds[@]} | tr -d \''"\' &
#wait  

#srun parallel -k --lb --jobs $njob "python $run_dir/correlation.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --nlast 3 --quantity stress --corrtype time > $SCRATCH/active-assembly-hoomd/log/stress_time_corr_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]} \
#                        ::: ${seeds[@]} | tr -d \''"\' &
#wait  

#srun parallel -k --lb --jobs $njob "python $run_dir/correlation.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --nlast 3 --quantity stress --corrtype space --rmax 15.0 > $SCRATCH/active-assembly-hoomd/log/stress_spatial_corr_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]} \
#                        ::: ${seeds[@]} | tr -d \''"\' &
#wait  

#echo "Getting velocity correlations..."
#srun parallel -k --lb --jobs $njob "python $run_dir/correlation.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --nlast 3 --quantity velocity --corrtype time > $SCRATCH/active-assembly-hoomd/log/vel_time_corr_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]} \
#                        ::: ${seeds[@]} | tr -d \''"\' &
#wait   

#srun parallel -k --lb --jobs $njob "python $run_dir/correlation.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --nlast 3 --quantity velocity --corrtype space --rmax 15.0 > $SCRATCH/active-assembly-hoomd/log/vel_spatial_corr_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]} \
#                        ::: ${seeds[@]} | tr -d \''"\' &
#wait   

echo "Doing pressure correlation analysis..."
srun parallel -k --lb --jobs $njob "python $run_dir/structure_factor.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --quantity pressure > $SCRATCH/active-assembly-hoomd/log/p2q_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\' &
wait   

echo "Doing strain correlation analysis..."
srun parallel -k --lb --jobs $njob "python $run_dir/structure_factor.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --quantity strain > $SCRATCH/active-assembly-hoomd/log/str2q_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\' &
wait  

echo "Doing structure factor analysis..."
srun parallel -k --lb --jobs $njob "python $run_dir/structure_factor.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --nchunks 5 --quantity density > $SCRATCH/active-assembly-hoomd/log/sq_network_kT={1}_va={2}_{3}_lambda={4}_seed={5}.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\' &
wait   

#Now do analysis over all trajectories

#echo "Averaging stress and strain correlations..."

#srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ strain_time_corr average postprocessed > $SCRATCH/active-assembly-hoomd/log/strain_time_corr_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]}  | tr -d \''"\' &
#wait

#srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ strain_spatial_corr average postprocessed > $SCRATCH/active-assembly-hoomd/log/strain_spatial_corr_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]}  | tr -d \''"\' &
#wait

#srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ stress_time_corr average postprocessed > $SCRATCH/active-assembly-hoomd/log/stress_time_corr_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]}  | tr -d \''"\' &
#wait

#srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ stress_spatial_corr average postprocessed > $SCRATCH/active-assembly-hoomd/log/stress_spatial_corr_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]}  | tr -d \''"\' &
#wait

#echo "Averaging velocity correlations..."
#srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ velocity_time_corr average postprocessed > $SCRATCH/active-assembly-hoomd/log/vel_time_corr_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]}  | tr -d \''"\' &
#wait

#srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ velocity_spatial_corr average postprocessed > $SCRATCH/active-assembly-hoomd/log/vel_space_corr_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
#                        ::: ${kTs[@]} \
#                        ::: ${vas[@]} \
#                        ::: ${taus[@]} \
#                        ::: ${lambdas[@]}  | tr -d \''"\' &
#wait

echo "Averaging pressure correlations..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ pressure_corr_q average postprocessed > $SCRATCH/active-assembly-hoomd/log/p2q_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait

echo "Averaging strain correlations..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ strain_corr_q average postprocessed > $SCRATCH/active-assembly-hoomd/log/str2q_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait

echo "Averaging structure factor..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/va={2}/{3}/lambda={4}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ sq average postprocessed > $SCRATCH/active-assembly-hoomd/log/sq_network_kT={1}_va={2}_{3}_lambda={4}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait
