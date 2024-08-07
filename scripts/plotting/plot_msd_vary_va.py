import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.msd as msd
import AnalysisTools.trajectory_stats as stats

kT=0.0
vas=[0.1, 0.5, 1.0, 2.0]
#taus = [0.1, 1.0, 10.0, float('inf')]
#lambdas = [1.0, 3.0, 10.0, 30.0]
#phis = [0.1,0.4]
phis=[0.0]
#taus = [0.1, 1.0, 10.0, 100.0]#, float('inf')]
taus = [0.1, 1.0, 10.0]#, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0, 20.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'
potential='none'

numstring='all'
tmax=200.0
nchunks=1

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))
colors_lambda = mpl.cm.plasma(np.linspace(0,1,len(lambdas)))
colors_va = mpl.cm.viridis(np.linspace(0,1,len(vas)))

myxmax = np.pi

for phi in phis:

    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f' % (potential, kT, phi)

    fig, axs = plt.subplots(len(taus),len(lambdas),figsize=(7.0,4.0), sharex=True, sharey=True)
    for j in range(len(lambdas)):
        Lambda = lambdas[j]
        for i in range(len(taus)):
            for k in range(len(vas)):
                va = vas[k]
                if taus[i] != float('inf'):
                    tau = taus[i]/va
                else:
                    tau = taus[i]
                if tau==float('inf'):
                    thedir = basedir + '/va=%f/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (va, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
                else:
                    thedir = basedir + '/va=%f/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (va, tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
                msd_data = np.load(thedir + '/msd_tmax=%f_nchunks=%d_%s_avg.npz' % (tmax, nchunks, numstring))

                print(list(msd_data.keys()))
                msdavg = msd_data['msd_0_avg']
                msderr = msd_data['msd_0_stderr']
                times = msd_data['times_avg']
                label = r'$v_a=%.01f$' % va
                axs[i][j].plot(times/tau,msdavg,color=colors_va[k], label=label, linewidth=va, zorder=10-k)#, marker='o')
                #axs[j].fill_between(times, msdavg-2*msderr, msdavg+2*msderr, color=colors_tau[i], alpha=0.4)
            axs[i][0].set_ylabel(r'MSD')
            #axs[j].set_xlim([0,myxmax])
            axs[0][j].set_title(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
            axs[i][j].set_xscale('log')
            axs[i][j].set_yscale('log')
            axs[-1][j].set_xlabel(r'$t/\tau_{\text{a}}$')

            if j==len(lambdas)-1:
                ax2=axs[i][j].twinx()
                ax2.set_ylabel(r'$v_{\text{a}}\tau_{\text{a}}=%.01f$' % taus[i])
                ax2.get_xaxis().set_ticks([])
                ax2.get_yaxis().set_ticks([])
    axs[-1][-1].legend(fontsize=8, loc='upper right')
    
    plt.savefig('plots/2d/msd_%s_multipanel_vary_va_phi=%f_va=%f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()

   