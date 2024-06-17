import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.msd as msd
import AnalysisTools.trajectory_stats as stats

kT=0.0
va=1.0
#taus = [0.1, 1.0, 10.0, float('inf')]
#lambdas = [1.0, 3.0, 10.0, 30.0]
#phis = [0.1,0.4]
phis=[0.0]
taus = [0.1, 1.0, 10.0, 100.0]#, float('inf')]
lambdas = [0.0, 1.0, 3.0, 5.0, 10.0, 20.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'
potential='none'

numstring='all'
tmax=100.0
nchunks=1

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))
colors_lambda = mpl.cm.plasma(np.linspace(0,1,len(lambdas)))

myxmax = np.pi

for phi in phis:

    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)

    fig, axs = plt.subplots(len(lambdas),1,figsize=(3.0,7.0), sharex=True, sharey=True)
    for j in range(len(lambdas)):
        Lambda = lambdas[j]
        for i in range(len(taus)):
            tau = taus[i]
            if tau==float('inf'):
                thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            msd_data = np.load(thedir + '/msd_tmax=%f_nchunks=%d_%s_avg.npz' % (tmax, nchunks, numstring))

            print(list(msd_data.keys()))
            msdavg = msd_data['msd_0_avg']
            msderr = msd_data['msd_0_stderr']
            times = msd_data['times_avg']
            taulabel = r'$\tau_a=%.01f$' % taus[i]
            if tau==float('inf'):
                taulabel = r'$\tau_a=\infty$'
            axs[j].plot(times,msdavg/msdavg[1],color=colors_tau[i], label=taulabel)#, marker='o')
            #axs[j].fill_between(times, msdavg-2*msderr, msdavg+2*msderr, color=colors_tau[i], alpha=0.4)
        axs[j].set_ylabel(r'$MSD$')
        #axs[j].set_xlim([0,myxmax])
        axs[j].set_title(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
        axs[j].set_xscale('log')
        axs[j].set_yscale('log')
    axs[-1].legend(fontsize=8, loc='upper right')
    axs[-1].set_xlabel(r'$t$')
    plt.savefig('plots/2d/msd_%s_multipanel_vary_tau_phi=%f_va=%f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()

    #plot the other way
    fig, axs = plt.subplots(1,len(taus),figsize=(10.0,2.5), sharex=True, sharey=True)
    for j in range(len(lambdas)):
        Lambda = lambdas[j]
        for i in range(len(taus)):
            tau = taus[i]
            if tau==float('inf'):
                thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            msd_data = np.load(thedir + '/msd_tmax=%f_nchunks=%d_%s_avg.npz' % (tmax, nchunks, numstring))

            msdavg = msd_data['msd_0_avg']
            msderr = msd_data['msd_0_stderr']
            times = msd_data['times_avg']
            themax = np.max(msdavg)
            theargmax = np.argmax(msdavg)

            lambdalabel = r'$\lambda_a=%.01f$' % lambdas[j]

            axs[i].plot(times,msdavg/msdavg[1],color=colors_lambda[j], label=lambdalabel)#, marker='o')
            #axs[i].fill_between(times, msdavg-2*msderr, msdavg+2*msderr, color=colors_lambda[j], alpha=0.4)

            #axs[i].plot(times,sqavgnorm,color=colors_lambda[j], label=lambdalabel)
            #axs[i].fill_between(times, sqavgnorm-2*sqerrnorm, sqavgnorm+2*sqerrnorm, color=colors_lambda[j], alpha=0.4)
            #axs[i].scatter(times[theargmax], themaxnorm, c='black', marker='*', s=35.0,zorder=10)
            #axs[i].scatter(times[theargmax], themaxnorm, c=colors_lambda[j], marker='*', s=15.0, zorder=11)

            #axs[].set_title(r'$\lambda_{\text{a}}=%.01f$' % tau)
            #axs[i].set_xlim([0,myxmax])
            axs[i].set_xlabel(r'$t$')
            axs[i].set_xscale('log')
            axs[i].set_yscale('log')
        axs[0].set_ylabel(r'$MSD$')
        
    axs[-1].legend(fontsize=8, loc='upper right')
    
    #plt.tight_layout()
    plt.savefig('plots/2d/msd_%s_multipanel_vary_Lambda_phi=%f_va=%f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
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
            msd_data = np.load(thedir + '/msd_tmax=%f_nchunks=%d_%s_avg.npz' % (tmax, nchunks, numstring))

            msdavg = msd_data['msd_0_avg']
            msderr = msd_data['msd_0_stderr']
            times = msd_data['times_avg']
            
            axs.plot(times,msdavg/msdavg[1], label=r'$\lambda_a=%.01f$' % Lambda, color=colors[i])#, marker='o')
            #axs.fill_between(times, msdavg+2*msderr, msdavg-2*msderr, alpha=0.4, color=colors[i])
            #axs.scatter(times[1:-1],sqavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)
            #axs.plot(times[1:-1],sqavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)

            axs.set_xlabel(r'$t$')
            axs.set_ylabel(r'$MSD$')

            axs.legend(loc='upper right')

            cnt+=1
            
            #plt.xlim([0,myxmax])
            #axs.set_ylim([-0.01,200])
            axs.set_xscale('log')
            axs.set_yscale('log')
    #plt.yscale('log')
    #plt.tight_layout()
    plt.savefig('plots/2d/msd_%s_quenched_vary_lambda_phi=%.01f_va=%.01f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()
