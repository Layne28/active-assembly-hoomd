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

    phi = args.phi
    dim = args.dim
    out_folder = args.out_folder
    init_style = args.init_style
    seed = args.seed
    seed_file = args.seed_file
    seed_file = os.path.expandvars(seed_file)
    out_folder = os.path.expandvars(out_folder)
    Lx = args.L
    Ly = args.L
    if dim==3:
        Lz = args.L

    sigma = 1.0
    epsilon = 1.0
    kT = 0.5
    dt = 2e-4
    nsteps = int(1e6)
    freq = 10000

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    #Check that parameters have acceptable values
    if phi<0.0 or phi>1.0:
        print('Error: phi must be between 0 and 1!')
        exit()

    if not (dim==2 or dim==3):
        print('Error: can only work in dimensions 2 or 3.')
        exit()

    #Read seed from file
    seednum = seed
    with open(seed_file) as f:
        lines = f.readlines()
        seed_line = lines[seed-1]
        seed = int(seed_line.strip())
    print('Using random seed: %d' % seed)

    #Create simulation state
    #if len(GPUtil.getAvailable())>0:
    #    xpu = hoomd.device.GPU()
    #else:
    xpu = hoomd.device.CPU()
    simulation = hoomd.Simulation(device=xpu, seed=1)
    init_file = 'initial_configurations/lattice/lattice_init_style=%s_dim=%d_phi=%f_L=%f.gsd' % (init_style, dim, phi, Lx)
    simulation.create_state_from_gsd(filename=init_file)

    #Set up integrator
    integrator_eq = hoomd.md.Integrator(dt=dt)

    #Set up interaction potential
    cell = hoomd.md.nlist.Cell(buffer=0.4)
    wca = hoomd.md.pair.LJ(nlist=cell, default_r_cut=sigma*2.0**(1.0/6.0))
    wca.params[('A', 'A')] = dict(epsilon=epsilon, sigma=sigma)
    integrator_eq.forces.append(wca)

    #Use Brownian dynamics
    brownian = hoomd.md.methods.Brownian(filter=hoomd.filter.All(), kT=kT)
    integrator_eq.methods = [brownian]
    simulation.operations.integrator = integrator_eq

    #Draw initial velocities
    simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=kT)

    #Add logger
    logger = hoomd.logging.Logger(categories=['scalar', 'string'])
    logger.add(simulation, quantities=['timestep'])
    table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=freq),
                              logger=logger)
    simulation.operations.writers.append(table)

    #Run "randomization"
    print('randomizing trajectory...')
    simulation.run(nsteps)
    print('done')

    #Save randomized configuration
    hoomd.write.GSD.write(state=simulation.state, filename=(out_folder + '/random_dim=%d_phi=%f_L=%f_seed=%d.gsd' % (dim, phi, Lx, seednum)), mode='wb')
    

main()
