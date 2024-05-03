#!/bin/bash

rc=1.5

Lx=200.000000
Ly=200.000000
nx=400
ny=400
compressibility='compressible'
potential='wca'

interp="linear"

#phis=(0.100000 0.400000 0.700000)
phis=(0.100000)
kTs=(0.000000)
#vas=(0.100000 0.300000 1.000000 3.000000)
vas=(1.000000)
taus=("tau=0.100000" "tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
lambdas=(1.000000 3.000000 5.000000 10.000000)

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
                    python ~/AnalysisTools/AnalysisTools/trajectory_stats.py /pscratch/sd/l/lfrechet/active-assembly-hoomd/manyseed/wca/2d/kT=${kT}/phi=${phi}/va=${va}/${tau}/lambda=${lambda}/Lx=${Lx}_Ly=${Ly}/nx=${nx}_ny=${ny}/interpolation\=linear/compressible/exponential/ csd csd postprocessed --rc ${rc}
                done
            done
        done
    done
done