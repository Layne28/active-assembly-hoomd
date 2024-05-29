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

rc = 1.5

kT=0.0
phi=0.1
va=1.0
taus = [0.1, 1.0, 10.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'
potential='none'
nseed=10

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)

Lambda = lambdas[-2]
tau = taus[-1]
print('lambda:', Lambda, 'tau:', tau)
fig, ax = plt.subplots(1,1)
if tau==float('inf'):
    thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
else:
    thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
traj = io.load_traj(thedir + 'seed=1/prod/traj.gsd')
cluster_file = h5py.File(thedir + '/seed=1/prod/clusters_rc=%f.h5' % rc)
cids = cluster_file['data/cluster_ids']

#define colormap
maxnum = np.max(cids[-1,:])
print(maxnum)
mycolors = cm.get_cmap('Purples_r', maxnum)
newcolors=mycolors(np.linspace(0,1,maxnum))
#make the first few clusters distinct colors
newcolors[0,:-1] = mcolors.to_rgb('Red')
newcolors[1,:-1] = mcolors.to_rgb('Orange')
newcolors[2,:-1] = mcolors.to_rgb('Yellow')
newcolors[3,:-1] = mcolors.to_rgb('Green')
newcolors[4,:-1] = mcolors.to_rgb('Blue')
newcmp = ListedColormap(newcolors)

ax.scatter(traj['pos'][-1,:,0], traj['pos'][-1,:,1], s=0.3, linewidths=0, c=cids[-1,:],cmap=newcmp)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.xaxis.set_tick_params(labelbottom=False)
ax.yaxis.set_tick_params(labelleft=False)

plt.tight_layout()
plt.savefig('plots/2d/clusters_%s_phi=%.01f_va=%.01f_lambda=%.01f_tau=%.01f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lambda, tau, Lx, Ly), dpi=300, bbox_inches='tight')
