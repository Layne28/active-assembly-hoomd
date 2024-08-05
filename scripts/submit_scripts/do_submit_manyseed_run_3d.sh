#!/bin/bash
#Do production runs

nseed=1

phis=(0.02) # 0.4)
Ls=(64.0)
taus=(0.1 1.0 10.0 100.0 inf)
#Lambdas=(1.0 3.0 5.0 10.0 20.0)
Lambdas=(1.0 3.0 5.0 10.0)
vas=(1.0)
kTs=(0.0) # 0.2 0.3 0.5 1.0)
seeds=($(seq 1 $nseed))
potential=$1
compressibility="compressible"

for phi in "${phis[@]}"; do
    for L in "${Ls[@]}"; do
        for tau in "${taus[@]}"; do
            for va in "${vas[@]}"; do
                for kT in "${kTs[@]}"; do
                    for Lambda in "${Lambdas[@]}"; do
                        echo $phi $L $tau $va $Lambda
                        jobname=run_3d_${potential}_kT=${kT}_phi=${phi}_va=${va}_tau=${tau}_lambda=${Lambda}_L=${L}
                        sbatch -o $HOME/active-assembly-hoomd/log/${jobname}.o%j -e $HOME/active-assembly-hoomd/log/${jobname}.e%j $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_manyseed_run_3d.sh $nseed $phi $L $tau $va $Lambda $potential $compressibility $kT
                    done
                done
            done
        done
    done
done
