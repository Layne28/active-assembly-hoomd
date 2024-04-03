#!/bin/bash

if python $HOME/active-assembly-hoomd/scripts/check_complete.py "traj.gsd"; then
    echo success
else
    echo failure
fi