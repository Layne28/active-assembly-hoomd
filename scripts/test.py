#Randomize a lattice configuration by treating
#particles as WCA hard spheres

import hoomd
import gsd.hoomd
import numpy as np
import argparse
import os
#import GPUtil

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--phi",
                        help="Packing fraction",
                        type=float,
                        dest="phi",
                        default=0.4)
    
    parser.add_argument("-i", "--init_style",
                        help="'uniform' or 'close_packed'",
                        type=str,
                        dest="init_style",
                        default='uniform')
    
    parser.add_argument("-d", "--dim",
                        help="2 or 3",
                        type=int,
                        dest="dim",
                        default=2)
    
    parser.add_argument("-L", "--box_length",
                        help="linear size of box (assume square/cube)",
                        type=float,
                        dest="L",
                        default=50.0)
    
    parser.add_argument("-o", "--out_folder",
                        help="Folder to which to save file",
                        type=str,
                        dest="out_folder",
                        default="$SCRATCH/active-assembly-hoomd/initial_configurations/equil")
    
    parser.add_argument("-s", "--seed",
                        help="Random seed (indexes line in seed file)",
                        type=int,
                        dest="seed",
                        default=1)
    
    parser.add_argument("-r", "--seed_file",
                        help="File containing random seeds",
                        type=str,
                        dest="seed_file",
                        default="$HOME/master_seeds.txt")

    args = parser.parse_args()
    print(args)
main()
