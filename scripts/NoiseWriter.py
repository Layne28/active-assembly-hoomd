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
                f.create_dataset("/noise/timestep", data=np.array([time]), maxshape=(None,))
                f.create_dataset("/noise/value/x", data=noise[np.newaxis,0,...])#, maxshape=(None,))
                f.create_dataset("/noise/value/y", data=noise[np.newaxis,1,...])#, maxshape=(None,))
                if self._dim==3:
                    f.create_dataset("/noise/value/z", data=noise[np.newaxis,2,...])#, maxshape=(None,))
            else:
                f['/noise/timestep'].resize((f['/noise/timestep'].shape[0] + 1), axis=0)
                f['/nosie/timestep'][-1:] = time

                #f['/noise/value/x'].resize((f['/noise/value/x']))

