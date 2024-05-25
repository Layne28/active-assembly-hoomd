#Write active noise to hdf5 file

import numpy as np
import h5py 

class NoiseWriter():

    def __init__(self, dims, spacing, va, Lambda, tau, dt, out_folder):

        self._dims = dims
        self._dim = dims.shape[0]
        self._spacing = spacing
        self._va = va
        self._Lambda = Lambda
        self._tau = tau
        self._out_folder = out_folder
        self._dt = dt

        with h5py.File(out_folder + "/noise_traj.h5", "w") as f:

            f.create_group("/parameters")
            f.create_group("/grid")
            f.create_group("/noise")

            f.create_dataset("/grid/dimensions", data=dims)
            f.create_dataset("/grid/spacing", data=spacing)

            f.create_dataset("/parameters/va", data=va)
            f.create_dataset("/parameters/tau", data=tau)
            f.create_dataset("/parameters/Lambda", data=Lambda)
            f.create_dataset("/parameters/dt", data=dt)

    def write(self, noise, time):
        """Write noise array to file."""
        with h5py.File(self._out_folder + "/noise_traj.h5", "a") as f:
            if '/noise/value' not in f:
                if self._dim==2:
                    maxshape=(None,self._dims[0],self._dims[1])
                else:
                    maxshape=(None,self._dims[0],self._dims[1],self._dims[2])
                f.create_dataset("/noise/timestep", data=np.array([time]), maxshape=(None,))
                f.create_dataset("/noise/value/x", data=noise[np.newaxis,0,...], maxshape=maxshape)
                f.create_dataset("/noise/value/y", data=noise[np.newaxis,1,...], maxshape=maxshape)
                if self._dim==3:
                    f.create_dataset("/noise/value/z", data=noise[np.newaxis,2,...], maxshape=maxshape)
            else:
                if self._dim==2:
                    myshape=(1,0,0)
                else:
                    myshape=(1,0,0,0)
                f['/noise/timestep'].resize((f['/noise/timestep'].shape[0] + 1), axis=0)
                f['/noise/timestep'][-1] = time

                f['/noise/value/x'].resize(tuple(map(sum, zip(f['/noise/value/x'].shape, myshape))))
                f['/noise/value/x'][-1:,...] = noise[0,...]

                f['/noise/value/y'].resize(tuple(map(sum, zip(f['/noise/value/y'].shape, myshape))))
                f['/noise/value/y'][-1:,...] = noise[1,...]

                if self._dim==3:
                    f['/noise/value/z'].resize(tuple(map(sum, zip(f['/noise/value/z'].shape, myshape))))
                    f['/noise/value/z'][-1:,...] = noise[2,...]

