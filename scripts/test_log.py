#Run hoomd + active noise generator simulation

import hoomd
import gsd.hoomd
import numpy as np
import math
import argparse
import os
import datetime
#import GPUtil

from ActiveNoise import noise as ActiveNoiseGen
import ActiveNoiseForce as ActiveForce
import NoiseWriter

try:
    import cupy as cp
    CUPY_IMPORTED = True
except ImportError:
    CUPY_IMPORTED = False

class Time:
    def __init__(self, simulation):
        self.simulation = simulation

    @property
    def time(self):
        return self.simulation.operations.integrator.dt*self.simulation.timestep

class Status:
    def __init__(self, simulation):
        self.simulation = simulation

    @property
    def seconds_remaining(self):
        try:
            return (
                self.simulation.final_timestep - self.simulation.timestep
            ) / self.simulation.tps
        except ZeroDivisionError:
            return 0

    @property
    def etr(self):
        return str(datetime.timedelta(seconds=self.seconds_remaining))



def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-phi", "--phi",
                        help="Packing fraction",
                        type=float,
                        dest="phi",
                        default=0.4)
    
    parser.add_argument("-init", "--init_style",
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
                        default=200.0)
    
    parser.add_argument("-g", "--grid_size",
                        help="linear size of active noise grid",
                        type=int,
                        dest="grid_size",
                        default=400)

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
                        help="potential energy (wca or lj)",
                        type=str,
                        dest="potential",
                        default="wca")

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
    
    parser.add_argument("-n", "--in_folder",
                        help="Folder to look for input configurations",
                        type=str,
                        dest="in_folder",
                        default="$SCRATCH/active-assembly-hoomd/initial_configurations")

    parser.add_argument("-o", "--out_folder",
                        help="Folder to which to save file",
                        type=str,
                        dest="out_folder",
                        default="$SCRATCH/active-assembly-hoomd")
    
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

    phi = args.phi
    potential = args.potential
    grid_size = args.grid_size
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
    Lx = args.L
    Ly = args.L
    if dim==3:
        Lz = args.L

    #Set default parameter values
    kT = 0.0
    sigma = 1.0
    epsilon = 1.0
    nsteps=int(sim_time/dt)
    freq=int(record_time_freq/dt)
    stepChunkSize=int(50)
    littleChunkSize=50
    
    #Check that parameters have acceptable values
    if phi<0.0 or phi>1.0:
        print('Error: phi must be between 0 and 1!')
        exit()

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
    out_folder += '/phi=%f' % phi
    out_folder += '/va=%f' % va
    if math.isinf(tau):
        out_folder += '/quenched'
    else:
        out_folder += '/tau=%f' % tau
    out_folder += '/lambda=%f' % Lambda
    if dim==2:
        out_folder += '/Lx=%f_Ly=%f' % (Lx, Ly)
        out_folder += '/nx=%d_ny=%d' % (grid_size, grid_size)
    else:
        out_folder += '/Lx=%f_Ly=%f_Lz=%f' % (Lx, Ly, Lz)
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
        xpu = hoomd.device.CPU()
    else:
        print('Using CPU')
        xp = np
        xpu = hoomd.device.CPU()
    simulation = hoomd.Simulation(device=xpu, seed=seed)

    #Load initial configuration
    input_file = in_folder
    if init_style=='uniform':
        input_file += '/equil/random_dim=%d_phi=%f_L=%f_seed=%d.gsd' % (dim, phi, Lx, seednum)
    else:
        input_file += '/lattice/lattice_init_style=%s_dim=%d_phi=%f_L=%f.gsd'
    simulation.timestep = 0
    simulation.create_state_from_gsd(filename=input_file)
    print('timestep', simulation.timestep)

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

    #Write trajectory
    gsd_writer = hoomd.write.GSD(filename='./test.gsd',
                                 trigger=hoomd.trigger.Periodic(freq),
                                 mode='wb',
                                 filter=hoomd.filter.All())
    simulation.operations.writers.append(gsd_writer)

    #Add logger
    progress_logger = hoomd.logging.Logger(categories=['scalar', 'string'])
    logger = hoomd.logging.Logger()
    progress_logger.add(simulation, quantities=['timestep', 'tps'])
    logger.add(pot, quantities=['energies', 'forces', 'virials'])
    mytime = Time(simulation)
    progress_logger[('Time', 'time')] = (mytime, 'time', 'scalar')
    #logger[('Time', 'time')] = (mytime, 'time', 'scalar')
    logger[('Time', 'time')] = (lambda: simulation.operations.integrator.dt*simulation.timestep, 'scalar')
    #progress_logger
    table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=freq),
                              logger=progress_logger)
    simulation.operations.writers.append(table)

    gsd_writer.logger = logger

    simulation.run(20)

main()
