#!/bin/bash
#Submit analysis of active noise simulation 

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=24:00:00

njob=64

tmax=100.000000
nseed=50

potential="wca"
interp="linear"
compressibility="compressible"
cov_type="exponential"
d=2
Lx=200.000000
nx=400

rc=1.200000

#phis=(0.100000 0.400000)
phis=(0.100000)
kTs=(0.000000)
vas=(0.100000 0.500000 2.000000)
taus=("tau=0.100000" "tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
lambdas=(1.000000 3.000000 5.000000 10.000000)
seeds=($(seq 1 $nseed))

mydir=$SCRATCH

module load parallel
module load conda/Mambaforge-23.1.0-1
mamba activate hoomd

run_dir=${HOME}/AnalysisTools/AnalysisTools/
echo ${run_dir}

#Loop through vas

for va in "${vas[@]}"; do
    if (( $(echo "$va==2.000000" |bc -l) )); then
        taus=("tau=0.050000" "tau=0.500000" "tau=5.000000" "quenched")
    fi
    if (( $(echo "$va==0.500000" |bc -l) )); then
        taus=("tau=0.200000" "tau=2.000000" "tau=20.000000" "quenched")
    fi
    if (( $(echo "$va==0.200000" |bc -l) )); then
        taus=("tau=0.500000" "tau=5.000000" "tau=50.000000" "quenched")
    fi
    if (( $(echo "$va==0.100000" |bc -l) )); then
        taus=("tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
    fi

    #Do per-trajectory analysis first
    #echo "Doing energy analysis..."
    #srun parallel -k --lb --jobs $njob "python $run_dir/energy.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va=${va}/{3}/lambda={4}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd > $SCRATCH/active-assembly-hoomd/log/energy_kT={1}_phi={2}_va=${va}_{3}_lambda={4}_seed={5}.out" \
    #                        ::: ${kTs[@]} \
    #                        ::: ${phis[@]} \
    #                        ::: ${taus[@]} \
    #                        ::: ${lambdas[@]} \
    #                        ::: ${seeds[@]} | tr -d \''"\' &

    #wait

    #echo "Doing structure factor analysis..."
    #srun parallel -k --lb --jobs $njob "python $run_dir/structure_factor.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va=${va}/{3}/lambda={4}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --quantity density --nchunks 5 > $SCRATCH/active-assembly-hoomd/log/sq_kT={1}_phi={2}_va=${va}_{3}_lambda={4}_seed={5}.out" \
    #                        ::: ${kTs[@]} \
    #                        ::: ${phis[@]} \
    #                        ::: ${taus[@]} \
    #                        ::: ${lambdas[@]} \
    #                        ::: ${seeds[@]} | tr -d \''"\' &

    #wait   

    echo "Doing cluster analysis..."
    srun parallel -k --lb --jobs $njob "python $run_dir/cluster.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va=${va}/{3}/lambda={4}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={5}/prod/traj.gsd --rc ${rc} > $SCRATCH/active-assembly-hoomd/log/cluster_kT={1}_phi={2}_va=${va}_{3}_lambda={4}_seed={5}.out" \
                            ::: ${kTs[@]} \
                            ::: ${phis[@]} \
                            ::: ${taus[@]} \
                            ::: ${lambdas[@]} \
                            ::: ${seeds[@]} | tr -d \''"\' &
    wait

    #Now do analysis over all trajectories
    #echo "Averaging energies..."
    #srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va=${va}/{3}/lambda={4}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ 'energies_and_forces' average postprocessed > $SCRATCH/active-assembly-hoomd/log/energy_kT={1}_phi={2}_va=${va}_{3}_lambda={4}_avg.out" \
    #                        ::: ${kTs[@]} \
    #                        ::: ${phis[@]} \
    #                        ::: ${taus[@]} \
    #                        ::: ${lambdas[@]}  | tr -d \''"\' &
    #wait

    #echo "Averaging structure factor..."
    #srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va=${va}/{3}/lambda={4}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ sq average postprocessed > $SCRATCH/active-assembly-hoomd/log/sq_kT={1}_phi={2}_va=${va}_{3}_lambda={4}_avg.out" \
    #                        ::: ${kTs[@]} \
    #                        ::: ${phis[@]} \
    #                        ::: ${taus[@]} \
    #                        ::: ${lambdas[@]}  | tr -d \''"\' &
    #wait

    echo "Averaging cluster size distributions..."
    srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va=${va}/{3}/lambda={4}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ csd csd postprocessed --rc ${rc} > $SCRATCH/active-assembly-hoomd/log/csd_kT={1}_phi={2}_va=${va}_{3}_lambda={4}_avg.out" \
                            ::: ${kTs[@]} \
                            ::: ${phis[@]} \
                            ::: ${taus[@]} \
                            ::: ${lambdas[@]}  | tr -d \''"\' &
    wait
done