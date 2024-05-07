#!/bin/bash
#Submit analysis of density and noise cross-correlation

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=24:00:00

njob=32

nseed=50

potential="wca"
interp="linear"
compressibility="compressible"
cov_type="exponential"
d=2
Lx=200.000000
nx=400

phi=$1
#phis=(0.100000 0.400000 0.700000)
#phis=(0.100000 0.400000)
phis=($phi)
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
echo "Doing energy analysis..."
srun parallel -k --lb --jobs $njob "python $run_dir/energy.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={6}/prod/traj.gsd > $SCRATCH/active-assembly-hoomd/log/energy_kT={1}_phi={2}_va={3}_{4}_lambda={5}_seed={6}.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\' &

wait

echo "Doing structure factor analysis..."
srun parallel -k --lb --jobs $njob "python $run_dir/structure_factor.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={6}/prod/traj.gsd 5 > $SCRATCH/active-assembly-hoomd/log/sq_kT={1}_phi={2}_va={3}_{4}_lambda={5}_seed={6}.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\' &

wait   

echo "Doing cluster analysis..."
srun parallel -k --lb --jobs $njob "python $run_dir/cluster.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={6}/prod/traj.gsd > $SCRATCH/active-assembly-hoomd/log/cluster_kT={1}_phi={2}_va={3}_{4}_lambda={5}_seed={6}.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\' &
wait

#Now do analysis over all trajectories
echo "Averaging energies..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ 'energies_and_forces' average postprocessed > $SCRATCH/active-assembly-hoomd/log/energy_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait

echo "Averaging structure factor..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ sq average postprocessed > $SCRATCH/active-assembly-hoomd/log/sq_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait

echo "Averaging structure factor fluctuations..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ sq_var average postprocessed > $SCRATCH/active-assembly-hoomd/log/sq_var_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait

echo "Averaging structure factor trajectories..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ sq_traj average postprocessed > $SCRATCH/active-assembly-hoomd/log/sq_traj_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait

echo "Averaging cluster size distributions..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ csd csd postprocessed > $SCRATCH/active-assembly-hoomd/log/csd_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait
