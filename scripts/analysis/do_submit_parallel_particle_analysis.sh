#!/bin/bash

vas=(0.100000 0.300000 3.000000)

for va in "${vas[@]}"
do
    sbatch -J "analysis_va=$va" -o "analysis_va=$va.o%j" -e "analysis_va=$va.e%j" $HOME/active-assembly-hoomd/scripts/analysis/submit_parallel_particle_analysis.sh $va
done