import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.structure_factor as sq
import AnalysisTools.trajectory_stats as stats

kT=0.0
phi=0.1
va=1.0
#taus = [0.1, 1.0, 10.0, float('inf')]
#lambdas = [1.0, 3.0, 10.0, 30.0]
phis = [0.1,0.4]
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]
Lx=100.000000
Ly=100.000000
nx=200
ny=200
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
            sq_data = np.load(thedir + '/sq_avg.npz')
            sqavg = sq_data['sq_vals_1d_nlast_avg']
            sqerr = sq_data['sq_vals_1d_nlast_stderr']
            q1d = sq_data['qvals_1d_avg']
            themax = np.max(sqavg)
            theargmax = np.argmax(sqavg)
            taulabel = r'$\tau_a=%.01f$' % taus[i]
            if tau==float('inf'):
                taulabel = r'$\tau_a=\infty$'
            axs[j].plot(q1d,sqavg,color=colors_tau[i], label=taulabel)
            axs[j].fill_between(q1d, sqavg-2*sqerr, sqavg+2*sqerr, color=colors_tau[i], alpha=0.4)
            axs[j].scatter(q1d[theargmax], themax, c='black', marker='*', s=35.0,zorder=10)
            axs[j].scatter(q1d[theargmax], themax, c=colors_tau[i], marker='*', s=15.0, zorder=11)
        axs[j].set_ylabel(r'$S(q)$')
        axs[j].set_xlim([0,0.5])
    axs[-1].legend(fontsize=8, loc='upper right')
    axs[-1].set_xlabel(r'$q$')
    plt.savefig('plots/2d/sq_1d_multipanel_vary_tau_phi=%f_va=%f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
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
            sq_data = np.load(thedir + '/sq_avg.npz')
            sqavg = sq_data['sq_vals_1d_nlast_avg']
            sqerr = sq_data['sq_vals_1d_nlast_stderr']
            q1d = sq_data['qvals_1d_avg']
            themax = np.max(sqavg)
            theargmax = np.argmax(sqavg)
            axs.plot(q1d,sqavg, label=r'$\lambda_a=%.01f$' % Lambda, color=colors[i])
            axs.fill_between(q1d, sqavg+2*sqerr, sqavg-2*sqerr, alpha=0.4, color=colors[i])
            axs.scatter(q1d[theargmax], themax, c='black', marker='*', s=35.0,zorder=10)
            axs.scatter(q1d[theargmax], themax, c=colors[i], marker='*', s=15.0, zorder=11)
            #axs.scatter(q1d[1:-1],sqavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)
            #axs.plot(q1d[1:-1],sqavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)

            axs.set_xlabel(r'$q\sigma$')
            axs.set_ylabel(r'$S(q)$')

            axs.legend(loc='upper right')

            cnt+=1
            
            plt.xlim([0,0.5])
            #axs.set_ylim([-0.01,200])
    #plt.yscale('log')
    #plt.tight_layout()
    plt.savefig('plots/2d/sq_1d_quenched_vary_lambda_phi=%.01f_va=%.01f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()
