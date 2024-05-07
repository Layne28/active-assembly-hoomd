import numpy as np
import gsd.hoomd
import sys
import matplotlib.pyplot as plt

import AnalysisTools.particle_io as io

def main():

    particle_file = sys.argv[1]
    density_file = sys.argv[2]

    traj = io.load_traj(particle_file)
    density = np.load(density_file)['density']

    Lx = traj['edges'][0]
    Ly = traj['edges'][1]

    fig = plt.figure()
    plt.imshow(density[-1,:,:].T, cmap='Blues', origin='lower', extent=[-Lx/2.0, Lx/2.0, -Ly/2.0, Ly/2.0])
    plt.scatter(traj['pos'][-1,:,0], traj['pos'][-1,:,1], c='gray', alpha=0.5, linewidths=0, s=0.3)
    plt.savefig('density.png', dpi=1200)
    #plt.show()

main()
