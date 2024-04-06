#!/bin/bash
#Test submit analysis of active noise simulation
tmax=100.000000
nseed=10

potential="wca"
interp="linear"
compressibility="compressible"
cov_type="exponential"
d=2
Lx=200.000000
nx=400

phis=(0.100000 0.400000 0.700000)
kTs=(0.000000)
vas=(1.000000)
taus=(tau=0.100000 tau=1.000000 tau=10.000000 quenched)
lambdas=(1.000000 3.000000 10.000000 30.000000)
seeds=($(seq 1 $nseed))

mydir=$SCRATCH

run_dir=${HOME}/AnalysisTools/AnalysisTools/
echo ${run_dir}

#Do per-trajectory analysis first
parallel --dry-run -k --lb --jobs 128 "$run_dir/energy.py $SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={6}/prod/traj.gsd > $SCRATCH/active-assembly-hoomd/log/energy_kT={1}_phi={2}_va={3}_{4}_lambda={5}_seed={6}.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\'


parallel --dry-run -k --lb --jobs 128 "$run_dir/structure_factor.py $SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={6}/prod/traj.gsd > $SCRATCH/active-assembly-hoomd/log/sq_kT={1}_phi={2}_va={3}_{4}_lambda={5}_seed={6}.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\'

parallel --dry-run -k --lb --jobs 128 "$run_dir/cluster.py $SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={6}/prod/traj.gsd > $SCRATCH/active-assembly-hoomd/log/cluster_kT={1}_phi={2}_va={3}_{4}_lambda={5}_seed={6}.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\'

#Now do analysis over all trajectories
parallel --dry-run -k --lb --jobs 128 "$run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ 'energies_and_forces' average postprocessed > $SCRATCH/active-assembly-hoomd/log/energy_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} | tr -d \''"\'

parallel --dry-run -k --lb --jobs 128 "$run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ sq average postprocessed > $SCRATCH/active-assembly-hoomd/log/sq_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} | tr -d \''"\'

parallel --dry-run -k --lb --jobs 128 "$run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ sq_traj average postprocessed > $SCRATCH/active-assembly-hoomd/log/sq_traj_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} | tr -d \''"\'

parallel --dry-run -k --lb --jobs 128 "$run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ csd average postprocessed  > $SCRATCH/active-assembly-hoomd/log/csd_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\'

