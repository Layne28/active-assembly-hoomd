#!/bin/bash

Nx=96
Ny=112
nx=200
ny=200
compressibility='compressible'
potential='wca'

interp="linear"

kTs=(0.000000)
#vas=(0.100000 0.300000 1.000000 3.000000)
vas=(1.000000)
taus=("tau=0.100000" "tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
lambdas=(1.000000 3.000000 5.000000 10.000000)

mydir=$SCRATCH

for kT in "${kTs[@]}"
do
    for va in "${vas[@]}"
    do
        for tau in "${taus[@]}"
        do
            for lambda in "${lambdas[@]}"
            do
                python ~/AnalysisTools/AnalysisTools/trajectory_stats.py /pscratch/sd/l/lfrechet/active-assembly-hoomd/manyseed/fene/2d/kT=${kT}/va=${va}/${tau}/lambda=${lambda}/Nx=${Nx}_Ny=${Ny}/nx=${nx}_ny=${ny}/interpolation\=linear/compressible/exponential/ pressure_corr_q average postprocessed
            done
        done
    done
done