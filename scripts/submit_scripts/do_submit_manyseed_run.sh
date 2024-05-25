#!/bin/bash
#Do production runs

nseed=100

#phis=(0.1 0.4 0.7)
phis=(0.1 0.4)
#phis=(0.7)
#Ls=(50.0 100.0 200.0 400.0)
#Ls=(100.0 200.0)
Ls=(200.0)
taus=(0.1 1.0 10.0 100.0 inf)
Lambdas=(1.0 3.0 5.0 10.0)
vas=(1.0)
seeds=($(seq 1 $nseed))
potential=$1

for phi in "${phis[@]}"; do
    for L in "${Ls[@]}"; do
        for tau in "${taus[@]}"; do
            for va in "${vas[@]}"; do
                for Lambda in "${Lambdas[@]}"; do
                    echo $phi $L $tau $va $Lambda
                    jobname=run_2d_${potential}_kT=${kT}_phi=${phi}_va=${va}_tau=${tau}_lambda=${lambda}_L=${L}
                    sbatch -o $HOME/active-assembly-hoomd/log/${jobname}.o%j -e $HOME/active-assembly-hoomd/log/${jobname}.e%j $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_manyseed_run.sh $nseed $phi $L $tau $va $Lambda $potential
                done
            done
        done
    done
done
