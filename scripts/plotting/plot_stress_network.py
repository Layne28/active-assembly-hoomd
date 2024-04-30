import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import h5py

from matplotlib import cm
from matplotlib import colors as mcolors
from matplotlib.colors import ListedColormap

import AnalysisTools.structure_factor as sq
import AnalysisTools.trajectory_stats as stats
import AnalysisTools.particle_io as io

kT=0.0
va=1.0
taus = [0.1, 1.0, 10.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]
Nx=96
Ny=112
nx=200
ny=200
potential='fene'
interpolation='linear'
compressibility='compressible'
cov_type='exponential'
nseed=10

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/va=%f' % (potential, kT, va)

Lambda = lambdas[1]
tau = taus[-1]
print('lambda:', Lambda, 'tau:', tau)
fig, ax = plt.subplots(1,1)
if tau==float('inf'):
    thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
else:
    thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
traj = io.load_traj(thedir + 'seed=1/prod/traj.gsd')

#extract virial stress
traj['virial']
print(traj['edges'])

ax.scatter(traj['pos'][-1,:,0], traj['pos'][-1,:,1], s=1.0, linewidths=0, c=-(traj['virial'][-1,:,0]+traj['virial'][-1,:,3]+traj['virial'][-1,:,5])/3.0,cmap='RdBu_r', vmin=-2,vmax=2)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([-traj['edges'][0]/2,traj['edges'][0]/2])
ax.set_ylim([-traj['edges'][1]/2,traj['edges'][1]/2])
ax.xaxis.set_tick_params(labelbottom=False)
ax.yaxis.set_tick_params(labelleft=False)

plt.tight_layout()
plt.savefig('plots/2d/stress_%s_network_va=%.01f_lambda=%.01f_tau=%.01f_Nx=%d_Ny=%d.png' % (potential, va, Lambda, tau, Nx, Ny), dpi=600, bbox_inches='tight')
