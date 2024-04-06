#Run hoomd + active noise generator simulation for elastic network

import hoomd
import gsd.hoomd
import numpy as np
import math
import argparse
import os
#import GPUtil

from ActiveNoise import noise as ActiveNoiseGen
import ActiveNoiseForce as ActiveForce
import NoiseWriter

try:
    import cupy as cp
    CUPY_IMPORTED = True
except ImportError:
    CUPY_IMPORTED = False

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d", "--dim",
                        help="2 or 3",
                        type=int,
                        dest="dim",
                        default=2)
    
    parser.add_argument("-Nx", "--unit_cells_x",
                        help="no. of unit cells in x direction",
                        type=float,
                        dest="Nx",
                        default=24)

    parser.add_argument("-Ny", "--unit_cells_y",
                        help="no. of unit cells in y direction",
                        type=float,
                        dest="Ny",
                        default=28)

    parser.add_argument("-Nz", "--unit_cells_z",
                        help="no. of unit cells in z direction",
                        type=float,
                        dest="Nz",
                        default=0)
    
    parser.add_argument("-gx", "--grid_size_x",
                        help="size of active noise grid in x",
                        type=int,
                        dest="grid_size_x",
                        default=400)

    parser.add_argument("-gy", "--grid_size_y",
                        help="size of active noise grid in y",
                        type=int,
                        dest="grid_size_y",
                        default=400)

    parser.add_argument("-gz", "--grid_size_z",
                        help="size of active noise grid in z",
                        type=int,
                        dest="grid_size_z",
                        default=0)

    parser.add_argument("-c", "--cov_type",
                        help="active noise covariance type (exponential or gaussian)",
                        type=str,
                        dest="cov_type",
                        default="exponential")

    parser.add_argument("-v", "--va",
                        help="active velocity",
                        type=float,
                        dest="va",
                        default=1.0)
    
    parser.add_argument("-tau", "--tau",
                        help="active noise correlation time",
                        type=float,
                        dest="tau",
                        default=1.0)
    
    parser.add_argument("-l", "--lambda",
                        help="active noise correlation length",
                        type=float,
                        dest="Lambda",
                        default=1.0)
    
    parser.add_argument("-comp", "--compressibility",
                        help="compressible or incompressible",
                        type=str,
                        dest="compressibility",
                        default="compressible")
    
    parser.add_argument("-i", "--interpolation",
                        help="none or linear",
                        type=str,
                        dest="interpolation",
                        default="linear")
    
    parser.add_argument("-dt", "--dt",
                        help="timestep",
                        type=float,
                        dest="dt",
                        default=2.5e-4)

    parser.add_argument("-p", "--potential",
                        help="potential energy of bonds (harmonic or fene)",
                        type=str,
                        dest="potential",
                        default="harmonic")

    parser.add_argument("-f", "--record_time_freq",
                        help="time interval (in units t_LJ) at which to output configurations",
                        type=float,
                        dest="record_time_freq",
                        default=0.25)
    
    parser.add_argument("-t", "--sim_time",
                        help="total simulation time (in units t_LJ)",
                        type=float,
                        dest="sim_time",
                        default=1000)
    
    parser.add_argument("-o", "--out_folder",
                        help="Folder to which to save file",
                        type=str,
                        dest="out_folder",
                        default="$SCRATCH/active-assembly-hoomd/network")
    
    parser.add_argument("-s", "--seed",
                        help="Random seed (indexes line in seed file)",
                        type=int,
                        dest="seed",
                        default=1)
    
    parser.add_argument("-r", "--seed_file",
                        help="File containing random seeds",
                        type=str,
                        dest="seed_file",
                        default="$HOME/hoomd_seeds.txt")

    args = parser.parse_args()

    potential = args.potential
    cov_type = args.cov_type
    va = args.va
    tau = args.tau
    Lambda = args.Lambda
    compressibility = args.compressibility
    interpolation = args.interpolation
    dt = args.dt
    record_time_freq = args.record_time_freq
    sim_time = args.sim_time
    dim = args.dim
    out_folder = args.out_folder
    in_folder = args.in_folder
    init_style = args.init_style
    seed = args.seed
    seed_file = args.seed_file
    seed_file = os.path.expandvars(seed_file)
    out_folder = os.path.expandvars(out_folder)
    in_folder = os.path.expandvars(in_folder)
    print(in_folder)
    Nx = args.Nx
    Ny = args.Ny
    grid_size_x = args.grid_size_x
    grid_size_y = args.grid_size_y
    if dim==3:
        Nz = args.Nz
        grid_size_z = args.grid_size_z

    #Set default parameter values
    kT = 0.0
    sigma = 1.0
    epsilon = 1.0
    nsteps=int(sim_time/dt)
    freq=int(record_time_freq/dt)
    stepChunkSize=int(50)
    littleChunkSize=50
    
    #Check that parameters have acceptable values

    if not (dim==2 or dim==3):
        print('Error: can only work in dimensions 2 or 3.')
        exit()

    #Check for (arbitrary) parameter set for which we'll output active noise
    if va==1.0 and phi==0.1 and kT==0.0 and potential=='wca':
        do_output_noise = 1
    else:
        do_output_noise = 0

    #Read seed from file
    seednum = seed
    with open(seed_file) as f:
        lines = f.readlines()
        seed_line = lines[seed-1]
        seed = int(seed_line.strip())
    print('Using random seed: %d' % seed)

    #Make output folder
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    #Make subfolder for output
    out_folder_noise = out_folder + '/noise'
    out_folder_noise += '/%dd' % dim
    if math.isinf(tau):
        out_folder_noise += '/quenched'
    else:
        out_folder_noise += '/tau=%f' % tau
    out_folder_noise += '/lambda=%f' % Lambda
    if dim==2:
        out_folder_noise += '/nx=%d_ny=%d' % (grid_size, grid_size)
    else:
        out_folder_noise += '/nx=%d_ny=%d_nz=%d' % (grid_size, grid_size, grid_size)
    out_folder_noise += '/%s' % compressibility
    out_folder_noise += '/%s' % cov_type
    out_folder_noise += '/seed=%d' % seednum

    out_folder += '/%s' % potential
    out_folder += '/%dd' % dim
    out_folder += '/kT=%f' % kT
    out_folder += '/va=%f' % va
    if math.isinf(tau):
        out_folder += '/quenched'
    else:
        out_folder += '/tau=%f' % tau
    out_folder += '/lambda=%f' % Lambda
    if dim==2:
        out_folder += '/Nx=%f_Ny=%f' % (Nx, Ny)
        out_folder += '/nx=%d_ny=%d' % (grid_size, grid_size)
    else:
        out_folder += '/Nx=%f_Ny=%f_Nz=%f' % (Nx, Ny, Nz)
        out_folder += '/nx=%d_ny=%d_nz=%d' % (grid_size, grid_size, grid_size)
    out_folder += '/interpolation=%s' % interpolation
    out_folder += '/%s' % compressibility
    out_folder += '/%s' % cov_type
    out_folder += '/seed=%d' % seednum

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    with open(out_folder + '/seed_value.txt', 'w') as f:
        f.write('%d' % seed)

    out_folder += '/prod'
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    if do_output_noise==1 and not os.path.exists(out_folder_noise):
        os.makedirs(out_folder_noise)

    #check for GPU vs CPU and create simulation state
    if CUPY_IMPORTED:
        print('Using GPU')
        xp = cp
        xpu = hoomd.device.GPU()
    else:
        print('Using CPU')
        xp = np
        xpu = hoomd.device.CPU()
    simulation = hoomd.Simulation(device=xpu, seed=seed)

    ###############
    #Lattice initialization
    ###############
    #Set particle positions
    position = []
    a = 1.0 #lattice constant
    if dim==2:
        #initialize triangular lattice
        frame.configuration.box = [Nx*a, Ny*a*np.sqrt(3.0)/2.0, 0.0, 0, 0, 0]

    ###############
    #Production run
    ###############

    #Set up integrator
    integrator = hoomd.md.Integrator(dt=dt)

    #Set up interaction potential
    cell = hoomd.md.nlist.Cell(buffer=0.4)
    if potential=="wca":
        pot = hoomd.md.pair.LJ(nlist=cell, default_r_cut=sigma*2.0**(1.0/6.0))
    else:
        pot = hoomd.md.pair.LJ(nlist=cell, default_r_cut=sigma*2.5)
    pot.params[('A', 'A')] = dict(epsilon=epsilon, sigma=sigma)
    integrator.forces.append(pot)

    #Use Brownian dynamics
    brownian = hoomd.md.methods.Brownian(filter=hoomd.filter.All(), kT=kT)
    integrator.methods = [brownian]
    simulation.operations.integrator = integrator

    #Add custom active noise force
    params = {}
    params['N'] = grid_size
    params['dx'] = Lx/params['N']
    params['print_freq'] = freq
    params['do_output'] = 0
    params['output_freq'] = freq
    params['chunksize'] = int(min(littleChunkSize,stepChunkSize))
    params['lambda'] = Lambda
    params['tau'] = tau
    params['dim'] = dim
    params['nsteps'] = stepChunkSize #warning: don't make this too big
    params['dt'] = dt
    params['D'] = va**2
    params['cov_type'] = cov_type
    params['verbose'] = False
    if xp==cp:
        params['xpu'] = 'gpu'
    else:
        params['xpu'] = 'cpu'
    print('using %s for active noise' % params['xpu'])

    if dim==2:
        edges = xp.array([Lx,Ly,0.0])
    else:
        edges = xp.array([Lx,Ly,Lz])
    spacing = xp.array([params['dx'],params['dx'],params['dx']])

    #Write trajectory
    gsd_writer = hoomd.write.GSD(filename=out_folder + '/traj.gsd',
                                 trigger=hoomd.trigger.Periodic(freq),
                                 mode='wb',
                                 filter=hoomd.filter.All())
    simulation.operations.writers.append(gsd_writer)

    #Add logger
    progress_logger = hoomd.logging.Logger(categories=['scalar', 'string'])
    logger = hoomd.logging.Logger()
    progress_logger.add(simulation, quantities=['timestep', 'tps'])
    logger.add(pot, quantities=['energies', 'forces', 'virials'])
    logger[('Time', 'time')] = (lambda: simulation.operations.integrator.dt*simulation.timestep, 'scalar')
    table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=freq),
                              logger=progress_logger)
    simulation.operations.writers.append(table)

    gsd_writer.logger = logger

    #Run
    print('running...')
    #Treat quenched case separately
    if math.isinf(tau):
        print('quenched')
        if do_output_noise==1:
            if dim==2:
                newdims = np.array([grid_size, grid_size])
                newspacing = np.array([params['dx'], params['dx']])
            else:
                newdims = np.array([grid_size, grid_size, grid_size])
                newspacing = np.array([params['dx'], params['dx'], params['dx']])
            noise_writer = NoiseWriter.NoiseWriter(newdims, newspacing, va, Lambda, tau, dt, out_folder_noise)
        params['nsteps'] = 1
        params['chunksize'] = 1
        init_arr = xp.array([]) #will need to change this if we want restart files to be read in
        noisetraj, init_arr = ActiveNoiseGen.run(init_arr, **params)
        if do_output_noise==1:
            noise_writer.write(np.array(noisetraj[...,0]), simulation.timestep)  
        active_force = ActiveForce.ActiveNoiseForce(xp.array(noisetraj), params['chunksize'], edges, spacing, interpolation, simulation.device, is_quenched=1)
        integrator.forces.append(active_force)

        #add active force to logger
        logger.add(active_force, quantities=['forces'])
        gsd_writer.logger = logger

        #run simulation
        simulation.run(nsteps)
        print('done')
    else:
        nchunks = nsteps//stepChunkSize
        if do_output_noise==1:
            if dim==2:
                newdims = np.array([grid_size, grid_size])
                newspacing = np.array([params['dx'], params['dx']])
            else:
                newdims = np.array([grid_size, grid_size, grid_size])
                newspacing = np.array([params['dx'], params['dx'], params['dx']])
            noise_writer = NoiseWriter.NoiseWriter(newdims, newspacing, va, Lambda, tau, dt, out_folder_noise)
        step = 0
        for c in range(nchunks):
            step = c*stepChunkSize
            #print('Running chunk %d (%d timesteps)' % (c,stepChunkSize))
            if c==0: #will need to change this if we want restart files to be read in
                init_arr = xp.array([])

            #Create and output active force
            noisetraj, init_arr = ActiveNoiseGen.run(init_arr, **params)
            if step % freq == 0 and do_output_noise==1: #freq will never be less than stepChunkSize
                noise_writer.write(np.array(noisetraj[...,0]), simulation.timestep)
            active_force = ActiveForce.ActiveNoiseForce(xp.array(noisetraj), params['chunksize'], edges, spacing, interpolation, simulation.device)
            integrator.forces.append(active_force)

            #add active force to logger
            logger.add(active_force, quantities=['forces'])
            gsd_writer.logger = logger

            #run simulation
            simulation.run(stepChunkSize)
            logger.remove(active_force)
            #gsd_writer.flush()
            integrator.forces.remove(active_force)

        print('done')

main()
