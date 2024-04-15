#!/bin/bash
#Do production runs

nseed=100

#phis=(0.1 0.4 0.7)
phis=(0.1 0.4)
#phis=(0.7)
#Ls=(50.0 100.0 200.0 400.0)
Ls=(200.0)
taus=(0.1 1.0 10.0 inf)
Lambdas=(1.0 3.0 10.0 30.0)
vas=(1.0)
seeds=($(seq 1 $nseed))

for phi in "${phis[@]}"; do
    for L in "${Ls[@]}"; do
        for tau in "${taus[@]}"; do
            for va in "${vas[@]}"; do
                for Lambda in "${Lambdas[@]}"; do
                    echo $phi $L $tau $va $Lambda
                    sbatch $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_manyseed_run.sh $nseed $phi $L $tau $va $Lambda
                done
            done
        done
    done
done
