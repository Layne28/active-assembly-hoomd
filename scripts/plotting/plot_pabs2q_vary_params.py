import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.structure_factor as sq
import AnalysisTools.trajectory_stats as stats

potential='fene'
kT=0.0
va=1.0
#taus = [0.1, 1.0, 10.0, float('inf')]
#lambdas = [1.0, 3.0, 10.0, 30.0]
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]
Nx=96
Ny=112
nx=200
ny=200
interpolation='linear'
compressibility='compressible'
cov_type='exponential'

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/va=%f' % (potential, kT, va)

fig, axs = plt.subplots(len(lambdas),1,figsize=(3.0,7.0), sharex=True)
for j in range(len(lambdas)):
    Lambda = lambdas[j]
    for i in range(len(taus)):
        tau = taus[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        p2q_data = np.load(thedir + '/pressure_corr_q_avg.npz')
        p2qavg = p2q_data['pabs2q_vals_1d_nlast_avg']
        p2qerr = p2q_data['pabs2q_vals_1d_nlast_stderr']
        q1d = p2q_data['qvals_1d_avg']
        themax = np.max(p2qavg)
        theargmax = np.argmax(p2qavg)
        taulabel = r'$\tau_a=%.01f$' % taus[i]
        if tau==float('inf'):
            taulabel = r'$\tau_a=\infty$'
        axs[j].plot(q1d,p2qavg,color=colors_tau[i], label=taulabel)
        axs[j].fill_between(q1d, p2qavg-2*p2qerr, p2qavg+2*p2qerr, color=colors_tau[i], alpha=0.4, linewidth=0)
        #axs[j].scatter(q1d[theargmax], themax, c='black', marker='*', s=35.0,zorder=10)
        #axs[j].scatter(q1d[theargmax], themax, c=colors_tau[i], marker='*', s=15.0, zorder=11)
    axs[j].set_ylabel(r'$\langle | p_{\text{abs}}(q) |^2 \rangle$')
    axs[j].set_xlim([0,0.5])
    axs[j].set_title(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
    #axs[j].set_yscale('log')
axs[-1].legend(fontsize=8, loc='upper right')
axs[-1].set_xlabel(r'$q$')
plt.savefig('plots/2d/p2q_abs_1d_multipanel_vary_tau_va=%f_Nx=%d_Ny=%d.png' % (va, Nx, Ny), dpi=300, bbox_inches='tight')
plt.close()

#Quenched case
fig, axs = plt.subplots(1,1)
colors = mpl.cm.viridis(np.linspace(0,1,len(lambdas)))
cnt=0
for i in range(len(lambdas)):
    Lambda = lambdas[i]
    thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
    #data = p2q.rebin_p2q(thedir, nbins=num_bins)
    #p2q_data = stats.get_postprocessed_stats(data)
    p2q_data = np.load(thedir + '/pressure_corr_q_avg.npz')
    p2qavg = p2q_data['pabs2q_vals_1d_nlast_avg']
    p2qerr = p2q_data['pabs2q_vals_1d_nlast_stderr']
    q1d = p2q_data['qvals_1d_avg']
    themax = np.max(p2qavg)
    theargmax = np.argmax(p2qavg)
    axs.plot(q1d,p2qavg, label=r'$\lambda_a=%.01f$' % Lambda, color=colors[i])
    axs.fill_between(q1d, p2qavg+2*p2qerr, p2qavg-2*p2qerr, alpha=0.4, color=colors[i], linewidth=0)
    #axs.scatter(q1d[theargmax], themax, c='black', marker='*', s=35.0,zorder=10)
    #axs.scatter(q1d[theargmax], themax, c=colors[i], marker='*', s=15.0, zorder=11)
    #axs.scatter(q1d[1:-1],p2qavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)
    #axs.plot(q1d[1:-1],p2qavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)

    axs.set_yscale('log')

    axs.set_xlabel(r'$q\sigma$')
    axs.set_ylabel(r'$\langle | p_{\text{abs}}(q) |^2 \rangle$')

    axs.legend(loc='upper right')

    cnt+=1
    
    plt.xlim([0,0.5])
    #axs.set_ylim([-0.01,200])
#plt.yscale('log')
#plt.tight_layout()
plt.savefig('plots/2d/p2q_abs_1d_quenched_vary_lambda_va=%.01f_Nx=%d_Ny=%d.png' % (va, Nx, Ny), dpi=300, bbox_inches='tight')
plt.close()
