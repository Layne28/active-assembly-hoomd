import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.structure_factor as sq
import AnalysisTools.trajectory_stats as stats
import AnalysisTools.particle_io as io

kT=0.0
phi=0.1
va=1.0
taus = [0.1, 1.0, 10.0, float('inf')]
lambdas = [1.0, 3.0, 10.0, 30.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'
nseed=10

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)


for j in range(len(lambdas)):
    Lambda = lambdas[j]
    #for i in range(len(taus)):
    tau = taus[-1]
    print('lambda:', Lambda, 'tau:', tau)
    fig, axs = plt.subplots(2,5,figsize=(8,3.5), sharex=True, sharey=True)
    for s in range(nseed):
        print(s)
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        traj = io.load_traj(thedir + '/seed=%d/prod/traj.gsd' % (s+1))

        axs[s//5][s%5].scatter(traj['pos'][-1,:,0], traj['pos'][-1,:,1], s=0.3, linewidths=0)
        axs[s//5][s%5].set_aspect('equal')
        axs[s//5][s%5].set_xticks([])
        axs[s//5][s%5].set_yticks([])
        axs[s//5][s%5].xaxis.set_tick_params(labelbottom=False)
        axs[s//5][s%5].yaxis.set_tick_params(labelleft=False)

    plt.tight_layout()
    plt.savefig('plots/2d/final_configs_phi=%.01f_va=%.01f_lambda=%.01f_tau=%.01f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lambda, tau, Lx, Ly), dpi=300, bbox_inches='tight')
