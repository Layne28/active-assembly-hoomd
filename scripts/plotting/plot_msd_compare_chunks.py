import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.msd as msd
import AnalysisTools.trajectory_stats as stats

kT=0.0
phi=0.0
va=1.0
tau=100.0
Lambda=10.0

numstring='all'
tmax=200.0
nchunks=2

#taus = [0.1, 1.0, 10.0, float('inf')]
#lambdas = [1.0, 3.0, 10.0, 30.0]
#phis = [0.1]#,0.4]
#taus = [0.1, 1.0, 10.0, 100.0]#, float('inf')]
#lambdas = [0.0, 1.0, 3.0, 5.0, 10.0, 20.0]

Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'
potential='none'

colors = mpl.cm.plasma(np.linspace(0,1,nchunks))

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)

fig, axs = plt.subplots(1,1)

thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)

msd_data = np.load(thedir + '/msd_tmax=%f_nchunks=%d_%s_avg.npz' % (tmax, nchunks, numstring))

for i in range(nchunks):
    msdavg = msd_data['msd_%d_avg' % i]
    msderr = msd_data['msd_%d_stderr' % i]
    times = msd_data['times_avg']

    print(i)
    print(msdavg)
    print(times)

    if msdavg.shape[0] != times.shape[0]:
        msdavg = msdavg[:-1]

    axs.plot(times,msdavg/msdavg[1], label=r'chunk %d' % (i+1), color=colors[i], marker='o', linewidth=1.0, markersize=2)
#axs.fill_between(times, msdavg+2*msderr, msdavg-2*msderr, alpha=0.4, color=colors[i])
#axs.scatter(times[1:-1],sqavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)
#axs.plot(times[1:-1],sqavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)

axs.plot(times, times, color='black', linestyle='--', label=r'$t$')
axs.plot(times, 30*times**2, color='gray', linestyle=':', label=r'$t^2$')

axs.set_xlabel(r'$t$')
axs.set_ylabel(r'MSD')

axs.legend()#loc='upper right')

#plt.xlim([0,myxmax])
#axs.set_ylim([10**(-2),3.0])
#axs.set_ylim([0.5,100.0])
axs.set_xscale('log')
axs.set_yscale('log')
#plt.yscale('log')
#plt.tight_layout()
plt.savefig('plots/2d/msd_compare_chunks_%s_phi=%.01f_va=%.01f_tau=%.01f_lambda=%.01f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, tau, Lambda, Lx, Ly), dpi=300, bbox_inches='tight')
plt.close()
