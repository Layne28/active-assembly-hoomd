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
taus = [0.1, 1.0, 10.0, float('inf')]
modtaus = [[1.0, 10.0, 100.0, float('inf')],
#            [0.5, 5.0, 50.0, float('inf')],
            [0.2, 2.0, 20.0, float('inf')],
            [0.1, 1.0, 10.0, float('inf')]]#,
            #[0.05, 0.5, 5.0, float('inf')]]
lambdas = [1.0, 3.0, 5.0, 10.0]
#vas = [0.1, 0.2, 0.5, 1.0, 2.0]
vas = [0.1, 0.5, 1.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(vas)))

for phi in phis:

    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f' % (kT, phi)

    fig, axs = plt.subplots(len(lambdas),len(taus),figsize=(8.0,7.0), sharex=True)
    for j in range(len(lambdas)):
        Lambda = lambdas[j]
        for i in range(len(taus)):
            for k in range(len(vas)):
                va = vas[k]
                tau = taus[i]
                modtau = modtaus[k][i]
                if tau==float('inf'):
                    thedir = basedir + '/va=%f/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (va, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
                else:
                    thedir = basedir + '/va=%f/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (va, modtau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
                sq_data = np.load(thedir + '/sq_avg.npz')
                sqavg = sq_data['sq_vals_1d_nlast_avg']
                sqerr = sq_data['sq_vals_1d_nlast_stderr']
                q1d = sq_data['qvals_1d_avg']
                themax = np.max(sqavg)
                theargmax = np.argmax(sqavg)
                label = r'$v_a=%.01f$' % (va)
                axs[j][i].plot(q1d,sqavg,color=colors_tau[k], label=label)
                axs[j][i].fill_between(q1d, sqavg-2*sqerr, sqavg+2*sqerr, color=colors_tau[k], alpha=0.4)
                axs[j][i].scatter(q1d[theargmax], themax, c='black', marker='*', s=35.0,zorder=10)
                axs[j][i].scatter(q1d[theargmax], themax, c=colors_tau[k], marker='*', s=15.0, zorder=11)

                axs[j][i].set_xlim([0,1.0])
                if taus[i]==float('inf'):
                    axs[0][i].set_title(r'$v_{\text{a}}\tau_{\text{a}}=\infty$')
                else:
                    axs[0][i].set_title(r'$v_{\text{a}}\tau_{\text{a}}=%.01f$' % taus[i])
            axs[-1][i].set_xlabel(r'$q$')
            ax2 = axs[j][-1].twinx()
            ax2.set_ylabel(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
            #axs[j][-1].set_title(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
        axs[j][0].set_ylabel(r'$S(q)$')
    axs[-1][-1].legend(fontsize=8, loc='upper right')
    plt.tight_layout()
    plt.savefig('plots/2d/sq_1d_multipanel_vary_va_tau_phi=%f_va=%f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()

