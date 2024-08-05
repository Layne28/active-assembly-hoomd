#!/bin/bash
#Do production runs

nseed=50

phis=(0.1 0.4)
#phis=(0.7)
#Ls=(50.0 100.0 200.0 400.0)
Ls=(200.0)
taus=(0.1 1.0 10.0 100.0 inf)
Lambdas=(1.0 3.0 5.0 10.0)
vas=(0.1 0.5 2.0)
seeds=($(seq 1 $nseed))

for phi in "${phis[@]}"; do
    for L in "${Ls[@]}"; do
        for va in "${vas[@]}"; do
            if (( $(echo "$va==2.0" |bc -l) )); then
                taus=(0.05 0.5 5.0 inf)
            fi
            if (( $(echo "$va==0.5" |bc -l) )); then
                taus=(0.2 2.0 20.0 inf)
            fi
            #if (( $(echo "$va==0.3" |bc -l) )); then
            #    taus=(0.5 5.0 50.0 inf)
            #fi
            if (( $(echo "$va==0.1" |bc -l) )); then
                taus=(1.0 10.0 100.0 inf)
            fi
            for tau in "${taus[@]}"; do
                for Lambda in "${Lambdas[@]}"; do
                    echo $phi $L $tau $va $Lambda
                    jobname=run_2d_${potential}_kT=${kT}_phi=${phi}_va=${va}_tau=${tau}_lambda=${lambda}_L=${L}
                    sbatch -o $HOME/active-assembly-hoomd/log/${jobname}.o%j -e $HOME/active-assembly-hoomd/log/${jobname}.e%j $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_manyseed_run.sh $nseed $phi $L $tau $va $Lambda
                done
            done
        done
    done
done
