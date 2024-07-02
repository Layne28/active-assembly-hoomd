#!/bin/bash
#Do production runs

nseed=100
compressibility='incompressible'

Ls=(200.0)
taus=(0.1 1.0 10.0 100.0 inf)
Lambdas=(0.0 1.0 3.0 5.0 10.0 20.0)
#Lambdas=(0.0 20.0)
vas=(1.0)
seeds=($(seq 1 $nseed))

for L in "${Ls[@]}"; do
    for tau in "${taus[@]}"; do
        for va in "${vas[@]}"; do
            for Lambda in "${Lambdas[@]}"; do
                echo $phi $L $tau $va $Lambda
                jobname=run_single_particle_2d_va=${va}_tau=${tau}_lambda=${Lambda}_L=${L}_${compressibility}
                sbatch -o $HOME/active-assembly-hoomd/log/${jobname}.o%j -e $HOME/active-assembly-hoomd/log/${jobname}.e%j $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_single_particle_manyseed_run.sh $nseed $L $tau $va $Lambda $compressibility
            done
        done
    done
done
