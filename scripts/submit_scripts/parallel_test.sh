#!/bin/bash

phis=(0.1 0.4 0.7)
init_style="uniform"
Ls=(50.0 100.0 200.0 400.0)
seeds=($(seq 1 $1))

echo ${phis[@]}
echo ${seeds[@]}

parallel -k --dry-run python scripts/randomize.py --init_style ::: $init_style ::: --phi ::: ${phis[@]} ::: -L ::: ${Ls[@]} ::: --seed ::: ${seeds[@]}
