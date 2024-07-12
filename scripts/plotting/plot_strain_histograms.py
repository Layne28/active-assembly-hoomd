import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

kT=0.0
vas = [0.01, 0.03, 0.1, 0.3, 1.0]
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0, 20.0]
vataus = [0.01, 0.03, 0.1, 0.3, 1.0]
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
            data = np.load(thedir + '/strain_histo.npz')
            bins = data['bins']
            hist = data['hist_nlast']
            
            taulabel = r'$\tau_a=%.01f$' % taus[i]
            if tau==float('inf'):
                taulabel = r'$\tau_a=\infty$'
            axs[j][i].plot(bins,hist,color=colors_va[k], label=r'$v_{\text{a}}=%.02f$' % va)
            axs[j][i].set_xlim([-0.3, 0.3])
            axs[j][i].set_yscale('log')

        if i==0:
            axs[j][i].set_ylabel(r'$P(s)$')
        if j==len(lambdas)-1:
            axs[j][i].set_xlabel(r'$s$')
    
    #axs[j].set_yscale('log')
axs[0][0].legend(fontsize=8, loc='upper right')
plt.savefig('plots/2d/strain_histo_multipanel_Nx=%d_Ny=%d.png' % (Nx, Ny), dpi=600, bbox_inches='tight')
plt.close()

##################
#Plot w/ same va*taua

fig, axs = plt.subplots(len(lambdas),len(vataus),figsize=(7.0,7.0), sharex=True, sharey=True)
for j in range(len(lambdas)):
    Lambda = lambdas[j]
    for i in range(len(vataus)):
        vatau = vataus[i]
        for l in range(len(taus)):
            tau = taus[l]
            for k in range(len(vas)):
                va = vas[k]

                if va*tau == vatau:
                    if tau==float('inf'):
                        thedir = basedir + '/va=%f/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (va, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
                    else:
                        thedir = basedir + '/va=%f/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (va, tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
                    data = np.load(thedir + '/strain_histo.npz')
                    bins = data['bins']
                    hist = data['hist_nlast']
                    
                    taulabel = r'$\tau_a=%.01f$' % taus[i]
                    if tau==float('inf'):
                        taulabel = r'$\tau_a=\infty$'
                    axs[j][i].plot(bins,hist,color=colors_va[k], label=r'$v_{\text{a}}=%.02f$' % (va))
                    axs[j][i].legend(fontsize=6)
                    axs[j][i].set_xlim([-0.3, 0.3])
                    axs[j][i].set_yscale('log')

            if i==0:
                axs[j][i].set_ylabel(r'$P(s)$')
            if j==len(lambdas)-1:
                axs[j][i].set_xlabel(r'$s$')
            if j==0:
                axs[j][i].set_title(r'$v_{\text{a}}\tau_{\text{a}} = %.02f$' % (vatau))
            if i==len(vataus)-1:
                ax2 = axs[j][i].twinx()
                ax2.set_ylabel(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
                ax2.set_yticklabels('')
    
    #axs[j].set_yscale('log')
plt.savefig('plots/2d/strain_histo_va_tau_multipanel_Nx=%d_Ny=%d.png' % (Nx, Ny), dpi=600, bbox_inches='tight')
plt.close()