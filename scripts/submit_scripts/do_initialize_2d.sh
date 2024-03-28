#!/bin/bash

phis=(0.1 0.4 0.7)
init_styles=("uniform" "close_packed")
Ls=(50.0 100.0 200.0 400.0)

nseed=$1

for phi in "${phis[@]}"
do
    for style in "${init_styles[@]}"
    do
        for L in "${Ls[@]}"
        do
            python3 scripts/initialize.py -f $phi -d 2 -L $L -i $style
        done
    done
done