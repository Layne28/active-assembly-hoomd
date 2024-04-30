import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.trajectory_stats as stats

Lx=200.000000
Ly=200.000000
nx=400
ny=400
kT=0.0
va=1.0
#taus = [0.1, 1.0, 10.0, float('inf')]
#lambdas = [1.0, 3.0, 10.0, 30.0]
phis = [0.1,0.4]
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]

interpolation='linear'
compressibility='compressible'
cov_type='exponential'

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))

for phi in phis:

    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)

    fig, axs = plt.subplots(len(lambdas),1,figsize=(3.0,7.0), sharex=True)
    for j in range(len(lambdas)):
        Lambda = lambdas[j]
        for i in range(len(taus)):
            tau = taus[i]
            if tau==float('inf'):
                thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir + '/csd_avg.npz')
            histavg = data['hist_4_avg']
            histerr = data['hist_4_stderr']
            bins = data['bins_4_avg']
            #themax = np.max(histavg)
            #theargmax = np.argmax(sqavg)
            taulabel = r'$\tau_a=%.01f$' % taus[i]
            if tau==float('inf'):
                taulabel = r'$\tau_a=\infty$'
            axs[j].plot(bins,histavg,color=colors_tau[i], label=taulabel)
            axs[j].fill_between(bins, histavg-2*histerr, histavg+2*histerr, color=colors_tau[i], alpha=0.4)
            #axs[j].scatter(bins[theargmax], themax, c='black', marker='*', s=35.0,zorder=10)
            #axs[j].scatter(bins[theargmax], themax, c=colors_tau[i], marker='*', s=15.0, zorder=11)
        axs[j].set_ylabel(r'$P(n)$')
        #axs[j].set_xlim([0,0.5])
        axs[j].set_yscale('log')
        axs[j].set_xscale('log')
        axs[j].set_title(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
    axs[-1].legend(fontsize=8, loc='upper right')
    axs[-1].set_xlabel(r'$n$')
    plt.savefig('plots/2d/csd_multipanel_vary_tau_phi=%f_va=%f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()

    #Quenched case
    fig, axs = plt.subplots(1,1)
    colors = mpl.cm.viridis(np.linspace(0,1,len(lambdas)))
    #phis = [0.1,0.4]
    phis=[phi]
    cnt=0
    for phi in phis:
        for i in range(len(lambdas)):
            Lambda = lambdas[i]
            thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            #data = sq.rebin_sq(thedir, nbins=num_bins)
            #sq_data = stats.get_postprocessed_stats(data)
            data = np.load(thedir + '/csd_avg.npz')
            histavg = data['hist_4_avg']
            histerr = data['hist_4_stderr']
            bins = data['bins_4_avg']
            #themax = np.max(sqavg)
            #theargmax = np.argmax(sqavg)
            axs.plot(bins,histavg, label=r'$\lambda_a=%.01f$' % Lambda, color=colors[i])
            axs.fill_between(bins, histavg+2*histerr, histavg-2*histerr, alpha=0.4, color=colors[i])
            #axs.scatter(q1d[theargmax], themax, c='black', marker='*', s=35.0,zorder=10)
            #axs.scatter(q1d[theargmax], themax, c=colors[i], marker='*', s=15.0, zorder=11)

            axs.set_xlabel(r'$n$')
            axs.set_ylabel(r'$P(n)$')

            axs.legend(loc='upper right')

            cnt+=1
            
            #plt.xlim([0,0.5])
            #axs.set_ylim([-0.01,200])
    plt.yscale('log')
    plt.xscale('log')
    #plt.tight_layout()
    plt.savefig('plots/2d/csd_quenched_vary_lambda_phi=%.01f_va=%.01f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()
