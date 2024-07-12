import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

kT=0.0
vas = [0.01, 0.03, 0.1, 0.3, 1.0]
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0, 20.0]
Nx=96
Ny=112
nx=200
ny=200
interpolation='linear'
compressibility='compressible'
cov_type='exponential'

colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
#colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/fene/2d/kT=%f' % (kT)

fig, axs = plt.subplots(len(lambdas),len(taus),figsize=(7.0,7.0), sharex=True, sharey=True)
for j in range(len(lambdas)):
    Lambda = lambdas[j]
    for i in range(len(taus)):
        tau = taus[i]
        for k in range(len(vas)):
            va = vas[k]
            if tau==float('inf'):
                thedir = basedir + '/va=%f/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (va, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/va=%f/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (va, tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir + '/strain_time_corr_avg.npz')
            times = data['times_avg']
            corr = data['corr_avg']
            
            taulabel = r'$\tau_a=%.01f$' % taus[i]
            if tau==float('inf'):
                taulabel = r'$\tau_a=\infty$'
            axs[j][i].plot(times,corr/corr[0],color=colors_va[k], label=r'$v_{\text{a}}=%.02f$' % va)
            axs[j][i].set_ylim([-0.2,1.1])
            #axs[j][i].set_xlim([-0.3, 0.3])
            

        if i==0:
            axs[j][i].set_ylabel(r'$C_{ss}(t)$')
        if j==len(lambdas)-1:
            axs[j][i].set_xlabel(r'$t$')
    
    #axs[j].set_yscale('log')
axs[0][0].legend(fontsize=8, loc='upper right')
plt.savefig('plots/2d/strain_acf_network_multipanel_Nx=%d_Ny=%d.png' % (Nx, Ny), dpi=600, bbox_inches='tight')
plt.close()
