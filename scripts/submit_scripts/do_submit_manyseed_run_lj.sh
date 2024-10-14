#!/bin/bash
#Do production runs

nseed=4

phis=(0.4)
Ls=(200.0)
taus=(0.1 1.0 10.0 100.0 inf)
Lambdas=(1.0 3.0 10.0 20.0)
vas=(1.0 3.0 10.0 30.0)
kTs=(1.0)
epss=(1.0 3.0 10.0) # 30.0)
seeds=($(seq 1 $nseed))
potential="lj"
compressibility="incompressible"

for phi in "${phis[@]}"; do
    for L in "${Ls[@]}"; do
        for tau in "${taus[@]}"; do
            for va in "${vas[@]}"; do
                for kT in "${kTs[@]}"; do
                    for eps in "${epss[@]}"; do
                        for Lambda in "${Lambdas[@]}"; do
                            echo $phi $L $tau $va $Lambda $kT $eps
                            jobname=run_2d_${potential}_kT=${kT}_eps=${eps}_phi=${phi}_va=${va}_tau=${tau}_lambda=${Lambda}_L=${L}
                            sbatch -o $HOME/active-assembly-hoomd/log/${jobname}.o%j -e $HOME/active-assembly-hoomd/log/${jobname}.e%j $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_manyseed_run.sh $nseed $phi $L $tau $va $Lambda $potential $compressibility $kT $eps
                        done
                    done
                done
            done
        done
    done
done
