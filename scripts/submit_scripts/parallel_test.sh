#!/bin/bash

phis=(0.1 0.4 0.7)
init_style="uniform"
Ls=(50.0 100.0 200.0 400.0)
seeds=($(seq 1 $1))

echo ${phis[@]}
echo ${seeds[@]}

#parallel -k --results outdir python scripts/test.py --init_style ::: $init_style ::: --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]}
#parallel -k --dry-run python scripts/test.py --init_style ::: $init_style ::: --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]} ::: ">" log_${seeds[@]}_init_style=${seeds[@]}_phi=${phis[@]}.txt
parallel -k --lb "python scripts/test.py --phi {1} -L {2} > log_phi={1}_L={2}.out" \
                        ::: ${phis[@]} \
                        ::: ${Ls[@]} \