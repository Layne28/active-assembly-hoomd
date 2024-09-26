import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.structure_factor as sq
import AnalysisTools.trajectory_stats as stats

potential='fene'
kT=0.0
va=0.3
tau = 10.0
Lambda = 10.0
Nx=96
Ny=112
nx=200
ny=200
interpolation='linear'
compressibility='compressible'
cov_type='exponential'

nseed=24

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/va=%f' % (potential, kT, va)
thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)

fig = plt.figure()

for i in range(nseed):
    
    p2q_data = np.load(thedir + 'seed=%d/prod/pressure_corr_q.npz' % (i+1))
    p2qavg = p2q_data['p2q_vals_1d_nlast']
    q1d = p2q_data['qvals_1d']

    plt.plot(q1d,p2qavg)
    
    if p2qavg[0]>10**5:
        print(i+1)


p2q_data = np.load(thedir + '/pressure_corr_q_avg.npz')
p2qavg = p2q_data['p2q_vals_1d_nlast_avg']
p2qerr = p2q_data['p2q_vals_1d_nlast_stderr']
q1d = p2q_data['qvals_1d_avg']

plt.plot(q1d,p2qavg, color='black')

plt.ylabel(r'$\langle | p(q) |^2 \rangle$')
#axs[j].set_xlim([0,0.5])
plt.title(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
plt.yscale('log')
plt.xscale('log')
plt.xlabel(r'$q$')
plt.savefig('plots/2d/p2q_test_manyseed.png', dpi=300, bbox_inches='tight')
plt.close()
