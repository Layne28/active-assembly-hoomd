#!/bin/bash
#Submit analysis of active noise simulation

#SBATCH -A m4494
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=1:00:00

njob=64

nseed=100

potential=$1
phi=$2
nchunks=$3
use_one_only=$4
tmax=$5

numstring='all'
if [ "${use_one_only}" = "1" ]; then
    numstring='one'
fi 
echo $numstring

interp="linear"
compressibility="compressible"
cov_type="exponential"
d=2
Lx=200.000000
nx=400

#phis=(0.100000 0.400000 0.700000)
#phis=(0.100000 0.400000)
phis=($phi)
kTs=(0.000000)
vas=(1.000000)
#vas=($1)
taus=("tau=0.100000" "tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
#lambdas=(1.000000 3.000000 10.000000 30.000000)
lambdas=(0.000000 1.000000 3.000000 5.000000 10.000000 20.000000)
#lambdas=(0.000000 20.000000)
seeds=($(seq 1 $nseed))

mydir=$SCRATCH

module load parallel
module load conda/Mambaforge-23.1.0-1
mamba activate hoomd

run_dir=${HOME}/AnalysisTools/AnalysisTools/
echo ${run_dir}

#Do per-trajectory analysis first
echo "Getting per-trajectory MSDs..."
srun parallel -k --lb --jobs $njob "python $run_dir/msd.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed={6}/prod/traj.gsd --nchunks ${nchunks} --tmax ${tmax} --use_one_only ${use_one_only} > $SCRATCH/active-assembly-hoomd/log/msd_kT={1}_phi={2}_va={3}_{4}_lambda={5}_seed={6}.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]} \
                        ::: ${seeds[@]} | tr -d \''"\' &
wait

#Now do analysis over all trajectories
echo "Averaging MSDs..."
srun parallel -k --lb --jobs $njob "python $run_dir/trajectory_stats.py $SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT={1}/phi={2}/va={3}/{4}/lambda={5}/Lx=${Lx}_Ly=${Lx}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/ msd_tmax=${tmax}_nchunks=${nchunks}_${numstring} average postprocessed > $SCRATCH/active-assembly-hoomd/log/msd_kT={1}_phi={2}_va={3}_{4}_lambda={5}_avg.out" \
                        ::: ${kTs[@]} \
                        ::: ${phis[@]} \
                        ::: ${vas[@]} \
                        ::: ${taus[@]} \
                        ::: ${lambdas[@]}  | tr -d \''"\' &
wait
