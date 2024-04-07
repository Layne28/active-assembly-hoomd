#!/bin/bash

Lx=$1
Ly=$2
nx=$3
ny=$4
nseed=$5
compressibility=$6
potential=$7

interp="linear"

#phis=(0.100000 0.400000 0.700000)
phis=(0.100000)
kTs=(0.000000)
#vas=(0.100000 0.300000 1.000000 3.000000)
vas=(1.000000)
taus=(0.100000 1.000000 10.000000 inf)
lambdas=(1.000000 3.000000 10.000000 30.000000)

mydir=$SCRATCH

for phi in "${phis[@]}"
do
    for kT in "${kTs[@]}"
    do
        for va in "${vas[@]}"
        do
            for tau in "${taus[@]}"
            do
                for lambda in "${lambdas[@]}"
                do
                    particlename=2d_${potential}_analysis_single_particle_kT=${kT}_phi=${phi}_va=${va}_tau=${tau}_lambda=${lambda}_Lx=${Lx}_Ly=${Ly}_nx=${nx}_ny=${ny}_interpolation=${interp}_${compressibility}
                    noisename=2d_analysis_noise_kT=${kT}_phi=${phi}_va=${va}_tau=${tau}_lambda=${lambda}_Lx=${Lx}_Ly=${Ly}_nx=${nx}_ny=${ny}_interpolation=${interp}_${compressibility}

                    sbatch -J $particlename -o "log/$particlename.o%j" -e "log/$particlename.e%j" $HOME/active-assembly-hoomd/scripts/analysis/submit_multiseed_particle_analysis.sh ${mydir}/active-assembly-hoomd/${potential}/2d/kT=${kT}/phi=${phi}/va=${va}/tau=${tau}/lambda=${lambda}/Lx=${Lx}_Ly=${Ly}/nx=${nx}_ny=${ny}/interpolation=${interp}/${compressibility}/ $nseed

                    if [ "$phi" = "0.400000" ] && [ "$va" = "1.000000" ] && [ "$potential" = "wca" ]; then
                        sbatch -J $noisename -o "log/$noisename.o%j" -e "log/$noisename.e%j" $HOME/active-assembly-hoomd/scripts/analysis/submit_multiseed_noise_analysis.sh ${mydir}/active-assembly-hoomd/${potential}/2d/kT=${kT}/phi=${phi}/va=${va}/tau=${tau}/lambda=${lambda}/Lx=${Lx}_Ly=${Ly}/nx=${nx}_ny=${ny}/interpolation=${interp}/${compressibility}/ $nseed
                    fi
                done
            done
        done
    done
done