#!/bin/bash
#Do production re-runs

nseed=50

phis=(0.100000 0.400000)
#Ls=(50.0 100.0 200.0 400.0)
Ls=(200.000000)
taus=(0.100000 1.000000 10.000000 100.000000 inf)
Lambdas=(1.000000 3.000000 5.000000 10.000000)
vas=(1.000000)
seeds=($(seq 1 $nseed))
potential="wca"
kT=0.000000
d=2
interp="linear"
compressibility="compressible"
cov_type="exponential"
nx=400

for phi in "${phis[@]}"; do
    for L in "${Ls[@]}"; do
        for tau in "${taus[@]}"; do
            for va in "${vas[@]}"; do
                for Lambda in "${Lambdas[@]}"; do
                    for seed in "${seeds[@]}"; do
                        #echo $phi $L $va $tau $Lambda $seed
                        filename=$SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT=${kT}/phi=${phi}/va=${va}/tau=${tau}/lambda=${Lambda}/Lx=${L}_Ly=${L}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed=${seed}/prod/traj.gsd
                        if [ "$tau" = "inf" ]; then
                            filename=$SCRATCH/active-assembly-hoomd/manyseed/${potential}/${d}d/kT=${kT}/phi=${phi}/va=${va}/quenched/lambda=${Lambda}/Lx=${L}_Ly=${L}/nx=${nx}_ny=${nx}/interpolation=${interp}/${compressibility}/${cov_type}/seed=${seed}/prod/traj.gsd
                        fi
                        
                        if ! [ -f $filename ]; then
                            echo "Trajectory file does not exist!"
                            echo $filename
                        else

                            OUTPUT=$(python $HOME/active-assembly-hoomd/scripts/check_complete.py $filename)
                            if ! [ $OUTPUT -eq 250 ]; then
                                echo "Needs to be rerun!"
                                echo "Only $OUTPUT frames, should be 250"
                                echo $filename
                            fi
                        fi
                    done
                done
            done
        done
    done
done
