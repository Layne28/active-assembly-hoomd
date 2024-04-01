#Run hoomd + active noise generator simulation

import hoomd
import gsd.hoomd
import numpy as np

try:
    import cupy as cp
    from cupyx.scipy.ndimage import map_coordinates
    CUPY_IMPORTED = True
except ImportError:
    CUPY_IMPORTED = False

class ActiveNoiseForce(hoomd.md.force.Custom):

    def __init__(self, myfield, chunksize, edges, spacing, interpolation, device, is_quenched=0):
        super().__init__()
        self._field = myfield
        self._dim = myfield.shape[0]
        self._chunksize = chunksize
        self._edges = edges
        self._spacing = spacing
        self._nx = int(self._edges[0]/self._spacing[0])
        self._ny = int(self._edges[0]/self._spacing[0])
        self._device = device
        if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
            xp = np
        else:
            xp = cp
        self._x = xp.linspace(-self._edges[0]/2.0,self._edges[0]/2.0, self._nx, endpoint=False)+self._spacing[0]/2.0
        self._y = xp.linspace(-self._edges[1]/2.0,self._edges[1]/2.0, self._ny, endpoint=False)+self._spacing[1]/2.0
        if self._dim==3:
            xp.linspace(-self._edges[2]/2.0,self._edges[2]/2.0, self._nz, endpoint=False)+self._spacing[2]/2.0
        self._interpolation = interpolation
        self._is_quenched = is_quenched
        device_str = device.__class__.__name__.lower()
        self._local_force_str = device_str + '_local_force_arrays'
        self._local_snapshot_str = device_str + '_local_snapshot'
        if interpolation=='linear':
            #print('testing interpolation...')
            self.do_interpolation_test()
            #print('done')

    def _to_array(self, list_data):
        if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
            return np.array(list_data)

        return cp.array(list_data)

    def set_forces(self, timestep):
        """Set the forces."""
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
            if self._is_quenched==1:
                arrays.force[:] = self.get_force_from_noise(pos, 0)
            else:
                arrays.force[:] = self.get_force_from_noise(pos, timestep % self._chunksize)

    def do_interpolation_test(self):

        if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
            xp = np
            Lx = self._edges[0]
            Ly = self._edges[1]
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

        if isinstance(self._device, hoomd.device.CPU) or not CUPY_IMPORTED:
            xp = np
        else:
            xp = cp
        
        force = xp.zeros(pos.shape)
        
        if self._interpolation=='linear':
            # linear interpolation
            scaled_pos = xp.divide((pos+0.5*self._edges), self._spacing)[:,:self._dim] - 0.5
            if self._dim==2:
                force[:,0] = map_coordinates(self._field[0,:,:,t], scaled_pos.T, order=1, mode='grid-wrap')
                force[:,1] = map_coordinates(self._field[1,:,:,t], scaled_pos.T, order=1, mode='grid-wrap')
            else:
                force[:,0] = map_coordinates(self._field[0,:,:,:,t], scaled_pos.T, order=1, mode='grid-wrap')
                force[:,1] = map_coordinates(self._field[1,:,:,:,t], scaled_pos.T, order=1, mode='grid-wrap')
                force[:,2] = map_coordinates(self._field[2,:,:,:,t], scaled_pos.T, order=1, mode='grid-wrap')

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
