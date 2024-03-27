import hoomd
import gsd.hoomd
import numpy as np
import sys
import GPUtil

#sys.path.insert(0, '/home/lfrechette/research/ActiveNoise')

#import ActiveNoise as an
from ActiveNoise import noise as an

try:
    import cupy as cp
    CUPY_IMPORTED = True
except ImportError:
    CUPY_IMPORTED = False

class myCustomForce(hoomd.md.force.Custom):

    def __init__(self, myfield, chunksize, edges, spacing, interpolation, device):
        super().__init__()
        self._field = myfield
        self._dim = myfield.shape[0]
        self._chunksize = chunksize
        self._edges = edges
        self._spacing = spacing
        self._device = device
        self._interpolation = interpolation
        device_str = device.__class__.__name__.lower()
        self._local_force_str = device_str + '_local_force_arrays'
        self._local_snapshot_str = device_str + '_local_snapshot'
        self.do_interpolation_test()

    def _to_array(self, list_data):
        if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
            return np.array(list_data)

        return cp.array(list_data)

    def set_forces(self, timestep):
        """Set the forces."""
        #print(timestep)
        # handle the case where cupy is not imported on the GPU
        if not CUPY_IMPORTED and isinstance(self._device, hoomd.device.GPU):
            return

        with getattr(self, self._local_force_str) as arrays, getattr(
            self._state, self._local_snapshot_str
        ) as snap:

            #Need to look up force on each particle depending on its position
            if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
                pos = np.array(snap.particles.position, copy=False)
            else:
                pos = cp.array(snap.particles.position, copy=False)
            arrays.force[:] = self.get_force_from_noise(pos, timestep % self._chunksize)

    def do_interpolation_test(self):

        if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
            xp = np
        else:
            xp = cp
        
        Lx = self._edges[0].get()
        Ly = self._edges[1].get()

        pos = xp.array([-Lx/2.0,-Ly/2.0,0.0])
        pos = pos[xp.newaxis,:]
        noise_force = self.get_force_from_noise(pos, 0)

        #Do interpolation by hand to test
        thenoise_x1 = self._field[0,-1,0,0]*0.5 + self._field[0,0,0,0]*0.5
        thenoise_x2 = self._field[0,-1,-1,0]*0.5 + self._field[0,0,-1,0]*0.5
        thenoise_x = thenoise_x1*0.5 + thenoise_x2*0.5

        thenoise_y1 = self._field[1,-1,0,0]*0.5 + self._field[1,0,0,0]*0.5
        thenoise_y2 = self._field[1,-1,-1,0]*0.5 + self._field[1,0,-1,0]*0.5
        thenoise_y = thenoise_y1*0.5 + thenoise_y2*0.5

        if xp.abs(noise_force[0,0]-thenoise_x)>1e-10 or xp.abs(noise_force[0,1]-thenoise_y)>1e-10:
            print('ERROR: active noise interpolation not working')
            print('from function:', noise_force)
            print('by hand:', thenoise_x, thenoise_y)

    def get_force_from_noise(self, pos, t):

        #if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
        #    force = np.zeros(pos.shape)
        #else:
        #    force = cp.zeros(pos.shape)

        if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
            xp = np
        else:
            xp = cp

        force = xp.zeros(pos.shape)
        
        if self._interpolation=='linear':
            # linear/bilinear/trilinear interpolation

            #only works for dim=2 right now!
            scaled_pos = xp.divide((pos+0.5*self._edges), self._spacing)[:,:self._dim]
            closest_index = xp.round(scaled_pos)
            ind1 = xp.zeros(scaled_pos.shape).astype(int)
            ind2 = xp.zeros(scaled_pos.shape).astype(int)
            ell = xp.zeros(scaled_pos.shape)
            for d in range(self._dim):
                ind1[:,d][closest_index[:,d]-scaled_pos[:,d]>0] = scaled_pos[:,d][closest_index[:,d]-scaled_pos[:,d]>0].astype(int)
                ind2[:,d][closest_index[:,d]-scaled_pos[:,d]>0] = xp.remainder((ind1[:,d][closest_index[:,d]-scaled_pos[:,d]>0]+1), xp.array(self._field.shape)[d+1])
                ind2[:,d][closest_index[:,d]-scaled_pos[:,d]<=0] = scaled_pos[:,d][closest_index[:,d]-scaled_pos[:,d]<=0].astype(int)
                ind1[:,d][closest_index[:,d]-scaled_pos[:,d]<=0] = xp.remainder((ind2[:,d][closest_index[:,d]-scaled_pos[:,d]<=0]-1 + xp.array(self._field.shape)[d+1]), xp.array(self._field.shape)[d+1])
                ell[:,d][closest_index[:,d]-scaled_pos[:,d]>0] = scaled_pos[:,d][closest_index[:,d]-scaled_pos[:,d]>0] - xp.floor(scaled_pos[:,d][closest_index[:,d]-scaled_pos[:,d]>0]) - 0.5
                ell[:,d][closest_index[:,d]-scaled_pos[:,d]<=0] = scaled_pos[:,d][closest_index[:,d]-scaled_pos[:,d]<=0] - xp.floor(scaled_pos[:,d][closest_index[:,d]-scaled_pos[:,d]<=0]) + 0.5
            for d in range(self._dim):
                f11 = self._field[d,ind1[:,0],ind1[:,1],t]
                f12 = self._field[d,ind1[:,0],ind2[:,1],t]
                f21 = self._field[d,ind2[:,0],ind1[:,1],t]
                f22 = self._field[d,ind2[:,0],ind2[:,1],t]
                fx1 = xp.multiply(ell[:,0], f21) + xp.multiply(1-ell[:,0], f11)
                fx2 = xp.multiply(ell[:,0], f22) + xp.multiply(1-ell[:,0], f12)
                fxy = xp.multiply(ell[:,1], fx2) + xp.multiply(1-ell[:,1], fx1) 
                force[:,d] = fxy
        else:
            #Nearest-neighbor interpolation
            if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
                all_indices = np.divide((pos + 0.5*self._edges), self._spacing).astype(int)
            else:
                all_indices = cp.divide((pos + 0.5*self._edges), self._spacing).astype(int)
            if self._dim==1:
                force[:,:self._dim] = self._field[:,all_indices[:,0],t].T
            elif self._dim==2:
                force[:,:self._dim] = self._field[:,all_indices[:,0],all_indices[:,1],t].T
            else:
                force[:,:self._dim] = self._field[:,all_indices[:,0],all_indices[:,1],all_indices[:,2],t].T

        return force

def main():

    #Set default parameter values
    kT = 1.0
    sigma = 1.0
    epsilon = 1.0
    nx = 24
    ny = 28
    a = 1.3 #lattice constant
    init_with_phi = 1 #use packing fraction to initialize particles
    phi = 0.1 #packing fraction
    Lx = 100.0
    Ly = 100.0
    activity = 0.0
    dt = 5e-4
    nsteps=int(1e6)#1e6
    stepChunkSize=int(50)
    littleChunkSize=50
    freq=100

    if len(GPUtil.getAvailable())>0:
        print('Using GPU for active noise')
        xp = cp
        #if params['xpu']=='gpu':
        #    print('Using GPU for active noise')
        #    xp = cp
        #else:
        #    print('Using CPU for active noise')
        #    xp = np
    else:
        print('Using CPU for active noise')
        xp = np

    #Set initial particle positions
    frame = gsd.hoomd.Frame()
    if init_with_phi==1:
        volume = Lx*Ly#nx*ny*np.sqrt(3.0)/2.0
        particle_volume = np.pi*(sigma/2)*(sigma/2)
        N = int(np.round(phi*volume/particle_volume))
        position = []
        for i in range(int(Lx)):
            for j in range(int(Ly)):
                x = i-Lx/2
                if (j%2==1):
                    x += 0.5
                y = (np.sqrt(3.0)/2.0)*(j-Ly/2)
                if i*ny+j<N:
                    position.append((x,y,0))
        frame.configuration.box = [Lx, Ly, 0.0, 0, 0, 0]
    else:
        N = nx*ny
        position = []
        for i in range(nx):
            for j in range(ny):
                x = a*i-nx*a/2
                if (j%2==1):
                    x += 0.5*a
                y = (np.sqrt(3.0)/2.0)*(a*j-ny*a/2)
                position.append((x,y,0))
        frame.configuration.box = [a*nx, a*ny*np.sqrt(3.0)/2.0, 0.0, 0, 0, 0]

    frame.particles.N = N
    frame.particles.position = position[0:N]
    frame.particles.types = ['A']
    with gsd.hoomd.open(name='lattice.gsd', mode='w') as f:
        f.append(frame)
    print('created lattice')

    #Create simulation state
    if len(GPUtil.getAvailable())>0:
        xpu = hoomd.device.GPU()
    else:
        xpu = hoomd.device.CPU()
    simulation = hoomd.Simulation(device=xpu, seed=1)
    simulation.create_state_from_gsd(filename='lattice.gsd')

    #Set up integrator
    integrator_eq = hoomd.md.Integrator(dt=1e-4)

    #Set up interaction potential
    if N>1:
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

    #Run "randomization"
    print('randomizing trajectory...')
    #simulation.run(20000)
    print('done')

    #Save randomized configuration
    hoomd.write.GSD.write(state=simulation.state, filename='random.gsd', mode='wb')

    ###############
    #Production run
    ###############

    integrator = hoomd.md.Integrator(dt=dt)

    #Set up interaction potential again
    if N>1:
        cell = hoomd.md.nlist.Cell(buffer=0.4)
        wca = hoomd.md.pair.LJ(nlist=cell, default_r_cut=sigma*2.0**(1.0/6.0))
        wca.params[('A', 'A')] = dict(epsilon=epsilon, sigma=sigma)
        integrator.forces.append(wca)
    brownian = hoomd.md.methods.Brownian(filter=hoomd.filter.All(), kT=0)
    integrator.methods = [brownian]
    simulation.operations.integrator = integrator

    #Add custom active noise force
    params = {}
    params['N'] = 200
    params['dx'] = Lx/params['N']
    params['print_freq'] = 1000
    params['do_output'] = 0
    params['output_freq'] = 100
    params['chunksize'] = int(min(littleChunkSize,stepChunkSize))
    params['lambda'] = 3.0
    params['tau'] = 10.0
    params['dim'] = 2
    params['nsteps'] = stepChunkSize #warning: don't make this too big
    params['dt'] = dt
    params['D'] = 1.0
    params['cov_type'] = 'exponential'
    params['xpu'] = 'gpu'
    params['verbose'] = False
    interpolation = 'linear'

    """
    if len(GPUtil.getAvailable())>0:
        if params['xpu']=='gpu':
            print('Using GPU for active noise')
            xp = cp
        else:
            print('Using CPU for active noise')
            xp = np
    else:
        print('Using CPU for active noise')
        xp = np
    """
    edges = xp.array([Lx,Ly,0.0])
    spacing = xp.array([params['dx'],params['dx'],params['dx']])

    #Write trajectory
    gsd_writer = hoomd.write.GSD(filename='trajectory.gsd',
                                 trigger=hoomd.trigger.Periodic(freq),
                                 mode='wb',
                                 filter=hoomd.filter.All())
    simulation.operations.writers.append(gsd_writer)

    #Add logger
    logger = hoomd.logging.Logger(categories=['scalar', 'string'])
    logger.add(simulation, quantities=['timestep'])
    table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=freq),
                              logger=logger)
    simulation.operations.writers.append(table)

    #Run
    print('running...')
    nchunks = nsteps//stepChunkSize
    for c in range(nchunks):
        #print('Running chunk %d (%d timesteps)' % (c,stepChunkSize))
        #print('getting noise trajectory...')
        if c==0: #will need to change this if we want restart files to be read in
            init_arr = xp.array([])
        noisetraj, init_arr = an.run(init_arr, **params)
        #print('noise traj shape:', noisetraj.shape)
        my_custom_force = myCustomForce(xp.array(noisetraj), params['chunksize'], edges, spacing, interpolation, simulation.device)
        integrator.forces.append(my_custom_force)
        #print('doing particle dynamics...')
        simulation.run(stepChunkSize)
        integrator.forces.remove(my_custom_force)
    print('done')

main()
