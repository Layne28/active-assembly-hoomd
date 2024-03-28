#Create initial lattice configuration

import gsd.hoomd
import numpy as np
import argparse
import os

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
                    default="initial_configurations/lattice")

    args = parser.parse_args()

    phi = args.phi
    dim = args.dim
    out_folder = args.out_folder
    init_style = args.init_style
    Lx = args.L
    Ly = args.L
    if dim==3:
        Lz = args.L
    sigma = 1.0

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    #Check that parameters have acceptable values
    if phi<0.0 or phi>1.0:
        print('Error: phi must be between 0 and 1!')
        exit()

    if not (dim==2 or dim==3):
        print('Error: can only work in dimensions 2 or 3.')
        exit()

    a = 1.3 #lattice constant

    #Set initial particle positions
    frame = gsd.hoomd.Frame()
    position = []
    if dim==2:
        #initialize triangular lattice
        frame.configuration.box = [Lx, Ly, 0.0, 0, 0, 0]
        if init_style=='close_packed':
            volume = Lx*Ly
            particle_volume = np.pi*(sigma/2)*(sigma/2)
            N = int(np.round(phi*volume/particle_volume))
            position = []
            cnt = 0
            for i in range(int(Lx/(sigma*2**(1.0/6.0)))):
                for j in range(int(Ly/(sigma*2**(1.0/6.0))/(np.sqrt(3.0)/2.0))):
                    x = i*sigma*2**(1.0/6.0)-Lx/2
                    if (j%2==1):
                        x += 0.5
                    y = (np.sqrt(3.0)/2.0)*(j*sigma*2**(1.0/6.0))-Ly/2
                    if cnt<N:
                        position.append((x,y,0))
                    cnt += 1
            if len(position)!=N:
                print('Error: particles not counted properly!')
        else:
            nx = int(np.sqrt(np.sqrt(3.0)/2.0*phi*Lx*Ly))
            ny = int(2*nx/np.sqrt(3.0))
            N = nx*ny
            a = Lx/nx
            for i in range(nx):
                for j in range(ny):
                    x = i*a-Lx/2
                    if j%2==1:
                        x += 0.5*a
                    y = np.sqrt(3.0)/2.0*j*a-Ly/2
                    position.append((x,y,0))

    else:
        frame.configuration.box = [Lx, Ly, Lz, 0, 0, 0]
        volume = Lx*Ly*Lz
        particle_volume = (4.0/3.0)*np.pi*(sigma/2)**3
        N = int(np.round(phi*volume/particle_volume))
        position = []

        if init_style=='close_packed':
            for i in range(int(Lx)):
                for j in range(int(Ly)):
                    for k in range(int(Lz)):
                        #simple cubic for now
                        x = i-Lx/2
                        y = j-Ly/2
                        z = k-Lz/2
                        if i*int(Ly)*int(Lz)+j*int(Ly)+k<N:
                            position.append((x,y,z))
                    

    frame.particles.N = N
    frame.particles.position = position[0:N]
    frame.particles.types = ['A']
    with gsd.hoomd.open(name=out_folder + '/lattice_init_style=%s_dim=%d_phi=%f_L=%f.gsd' % (init_style, dim, phi, Lx), mode='w') as f:
        f.append(frame)
    print('created lattice')

main()
