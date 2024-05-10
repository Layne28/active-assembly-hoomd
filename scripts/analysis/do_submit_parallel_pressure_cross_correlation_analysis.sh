#!/bin/bash

taus=("tau=0.100000" "tau=1.000000" "tau=10.000000" "tau=100.000000" "quenched")
lambdas=(1.000000 3.000000 5.000000 10.000000)

for tau in "${taus[@]}"
do
    for lambda in "${lambdas[@]}"
    do
        sbatch -J "cross_corr_tau=${tau}_lambda=${lambda}" -o "cross_corr_tau=${tau}_lambda=${lambda}.o%j" -e "cross_corr_tau=${tau}_lambda=${lambda}.e%j" $HOME/active-assembly-hoomd/scripts/analysis/submit_parallel_pressure_cross_correlation_analysis_manyseed_indiv_param.sh $tau $lambda
    done
done