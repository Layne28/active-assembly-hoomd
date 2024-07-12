#!/bin/bash
#Do production runs

nseed=20
potential="fene"

Nx=96 #192 #96
Ny=112 #224 #112
taus=(0.1 1.0 10.0 100.0 inf)
Lambdas=(1.0 3.0 5.0 10.0 20.0)
vas=(0.30)

for tau in "${taus[@]}"; do
    for va in "${vas[@]}"; do
        for Lambda in "${Lambdas[@]}"; do
            echo $tau $va $Lambda $potential
            jobname=run_network_2d_${potential}_kT=${kT}_Nx=${Nx}_Ny=${Ny}_va=${va}_tau=${tau}_lambda=${Lambda}
            sbatch -o $HOME/active-assembly-hoomd/log/${jobname}.o%j -e $HOME/active-assembly-hoomd/log/${jobname}.e%j $HOME/active-assembly-hoomd/scripts/submit_scripts/submit_manyseed_network_run.sh $nseed $Nx $Ny $tau $va $Lambda $potential
        done
    done
done
