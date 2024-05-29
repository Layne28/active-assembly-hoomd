import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

kT=0.0
phi=0.4
phis=[0.1,0.4]
va=1.0
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [0.0, 1.0, 3.0, 5.0, 10.0, 20.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'
potential='none'

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)

colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)+1))

#Collect correlation measurements
diff_arr = np.zeros((len(lambdas),len(taus)))
diff_err = np.zeros((len(lambdas),len(taus)))

fig, axs = plt.subplots(1,2,figsize=(6,2.75), sharex=True, sharey=True)
for p in range(len(phis)):
    phi = phis[p]
    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)
    for i in range(len(lambdas)):
        for j in range(len(taus)):
            tau = taus[j]
            Lambda = lambdas[i]
            if tau==float('inf'):
                thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir+'/density_noise_correlation_avg.npz')
            diff_arr[i,j] = data['noise_mag_conditional_diff_avg']
            diff_err[i,j] = data['noise_mag_conditional_diff_stderr']
    print(diff_arr)
    for j in range(len(taus)):
        taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
        if taus[j]==float('inf'):
            taulabel=r'$\tau_a=\infty$'
        axs[p].errorbar(lambdas, diff_arr[:,j], yerr=2*diff_err[:,j], color=colors_tau[j], label=taulabel, marker='o', markersize=5.0, zorder=j)
    axs[p].axhline(y=0.0, color='black', linestyle='--')
    axs[p].set_title(r'$\phi=%.01f$' % phi)
    #axs[0][0].set_ylim([-0.005,0.0005])
    axs[1].legend(ncol=2, fontsize=8)#, loc='lower center')
    #axs[0][0].set_ylim([-0.0005,0.0005])
    axs[p].set_xlabel(r'$\lambda_{\text{a}}$')
    axs[0].set_ylabel(r'$\langle|\xi|(\mathbf{r}) \mid \rho(\mathbf{r})=1 \rangle - \langle|\xi|\rangle$')
#plt.suptitle('Density-noise magnitude cross correlation')
plt.savefig('plots/2d/%s_conditional_noise.png' % potential)
