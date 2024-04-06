#!/bin/bash
#Do production re-runs

nseed=10

phis=(0.100000 0.400000 0.700000)
#phis=(0.1 0.4)
#phis=(0.7)
#Ls=(50.0 100.0 200.0 400.0)
Ls=(200.000000)
taus=(0.100000 1.000000 10.000000 inf)
Lambdas=(1.000000 3.000000 10.000000 30.000000)
vas=(1.000000)
seeds=($(seq 1 $nseed))

for phi in "${phis[@]}"; do
    for L in "${Ls[@]}"; do
        for tau in "${taus[@]}"; do
            for va in "${vas[@]}"; do
                echo $phi $L $tau $va
                sbatch $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_rerun.sh $nseed $phi $L $tau $va
            done
        done
    done
done
