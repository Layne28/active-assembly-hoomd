#Create initial single particle configuration

import gsd.hoomd
import numpy as np
import argparse
import os

def main():

    parser = argparse.ArgumentParser()

    
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
                    default="initial_configurations/single_particle/")

    args = parser.parse_args()

    phi = 0.0
    dim = args.dim
    out_folder = args.out_folder
    Lx = args.L
    Ly = args.L
    if dim==3:
        Lz = args.L
    sigma = 1.0

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    #Check that parameters have acceptable values
    if not (dim==2 or dim==3):
        print('Error: can only work in dimensions 2 or 3.')
        exit()

    #Set initial particle positions
    frame = gsd.hoomd.Frame()
    position = []
    N = 1
    if dim==2:
        frame.configuration.box = [Lx, Ly, 0.0, 0, 0, 0]
        position=[(0.0,0.0,0.0)]
    else:
        frame.configuration.box = [Lx, Ly, Lz, 0, 0, 0]
        position=[(0.0,0.0,0.0)]
                    
    frame.particles.N = N
    frame.particles.position = position[0:N]
    frame.particles.types = ['A']
    with gsd.hoomd.open(name=out_folder + '/dim=%d_L=%f.gsd' % (dim, Lx), mode='w') as f:
        f.append(frame)
    print('created single particle')

main()
