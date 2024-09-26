#!/bin/bash
#Do production runs

nseed=100
compressibility='compressible'

Ls=(200.0)
taus=(10.0)
Lambdas=(3.0)
vas=(0.01 0.1 0.5 1.0 2.0 10.0)
seeds=($(seq 1 $nseed))

for L in "${Ls[@]}"; do
    for va in "${vas[@]}"; do
        for tau in "${taus[@]}"; do
            for Lambda in "${Lambdas[@]}"; do
                echo $phi $L $tau $va $Lambda
                jobname=run_single_particle_2d_va=${va}_tau=${tau}_lambda=${Lambda}_L=${L}_${compressibility}
                sbatch -o $HOME/active-assembly-hoomd/log/${jobname}.o%j -e $HOME/active-assembly-hoomd/log/${jobname}.e%j $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_single_particle_manyseed_run.sh $nseed $L $tau $va $Lambda $compressibility
            done
        done
    done
done
