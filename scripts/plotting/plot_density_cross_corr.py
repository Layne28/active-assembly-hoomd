import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

kT=0.0
phi=0.4
phis=[0.1,0.4]
va=1.0
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)

#Collect correlation measurements
corr_arr = np.zeros((len(lambdas),len(taus)))
corr_err = np.zeros((len(lambdas),len(taus)))
noise_arr = np.zeros((len(lambdas),len(taus)))
var_noise_arr = np.zeros((len(lambdas),len(taus)))
density_arr = np.zeros((len(lambdas),len(taus)))
for i in range(len(lambdas)):
    for j in range(len(taus)):
        tau = taus[j]
        Lambda = lambdas[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        data = np.load(thedir+'/density_noise_correlation_avg.npz')
        corr_arr[i,j] = data['one_point_corr_avg']
        corr_err[i,j] = data['one_point_corr_stderr']
        noise_arr[i,j] = data['mean_noise_avg']
        density_arr[i,j] = data['mean_density_avg']
#print(corr_arr)
#print(corr_err)


mymax = np.max(np.abs(corr_arr))
fig = plt.figure()
for i in range(len(lambdas)):
    for j in range(len(taus)):
        plt.scatter(lambdas[i], taus[j], c=corr_arr[i,j],cmap='RdBu_r',vmin=-mymax, vmax=mymax,linewidth=1, edgecolors='black', s=100)
plt.xlabel(r'$\lambda_{\text{a}}$')
plt.ylabel(r'$\tau_{\text{a}}$')
plt.yscale('log')
#plt.gca().set_aspect('equal')
plt.savefig('plots/2d/density_cross_corr_2d_phi=%.1f.png' % phi)

colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))
fig = plt.figure()
for j in range(len(taus)-1):
    taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
    if taus[j]==float('inf'):
        taulabel = r'$\tau_a=\infty$'
    #plt.plot(lambdas, corr_arr[:,j], color=colors_tau[j], label=taulabel, marker='o')
    #print(corr_arr.shape)
    #print(corr_err.shape)
    plt.errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
    #plt.errorbar(lambdas, corr_arr[:,j]/(noise_arr[:,j]*density_arr[:,j]), yerr=2*corr_err[:,j]/(noise_arr[:,j]*density_arr[:,j]), color=colors_tau[j], label=taulabel, marker='o',zorder=j)
if phi==0.4:
    plt.ylim([-0.009,0.004])
else:
    plt.ylim([-0.005,0.001])
plt.xlabel(r'$\lambda_{\text{a}}$')
plt.ylabel(r'$\langle \delta |\mathbf{\xi}| \delta \rho \rangle$')
plt.legend(loc='lower left', fontsize=9)
#plt.yscale('log')
#plt.gca().set_aspect('equal')
plt.savefig('plots/2d/density_cross_corr_phi=%.1f.png' % phi)




fig, axs = plt.subplots(2,2,figsize=(6,4.5), sharex=True, sharey='row')
for p in range(len(phis)):
    phi = phis[p]
    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)
    for i in range(len(lambdas)):
        for j in range(len(taus)):
            tau = taus[j]
            Lambda = lambdas[i]
            if tau==float('inf'):
                thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir+'/density_noise_correlation_avg.npz')
            corr_arr[i,j] = data['one_point_corr_norm_avg']
            corr_err[i,j] = data['one_point_corr_norm_stderr']
            noise_arr[i,j] = data['mean_noise_avg']
            density_arr[i,j] = data['mean_density_avg']
    for j in range(len(taus)-1):
        taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
        axs[0][p].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
        #axs[0][p].errorbar(lambdas, corr_arr[:,j]/np.max(np.abs(corr_arr[:,j])), yerr=2*corr_err[:,j]/np.max(np.abs(corr_arr[:,j])), color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
    axs[1][p].errorbar(lambdas, corr_arr[:,-1], yerr=2*corr_err[:,j], color='blue', label=r'$\tau_a=\infty$', marker='o')
    axs[0][p].axhline(y=0.0, color='black', linestyle='--')
    axs[1][p].axhline(y=0.0, color='black', linestyle='--')
    axs[0][p].set_title(r'$\phi=%.01f$' % phi)
    axs[0][0].legend(ncol=2, fontsize=8)#, loc='lower center')
    #axs[0][0].set_ylim([-0.0005,0.0005])
    axs[-1][0].legend()
    axs[-1][p].set_xlabel(r'$\lambda_{\text{a}}$')
    axs[1][0].set_ylabel(r'$\langle \delta |\xi| \delta \rho \rangle$')
    axs[0][0].set_ylabel(r'$\langle \delta |\xi| \delta \rho \rangle$')
plt.savefig('plots/2d/density_cross_corr_norm_multipanel.png')



#Alternative multipanel
fig, axs = plt.subplots(len(taus),2,figsize=(6,9), sharex=True, sharey='row')
for p in range(len(phis)):
    phi = phis[p]
    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)
    for i in range(len(lambdas)):
        for j in range(len(taus)):
            tau = taus[j]
            Lambda = lambdas[i]
            if tau==float('inf'):
                thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir+'/density_noise_correlation_avg.npz')
            corr_arr[i,j] = data['one_point_corr_norm_avg']
            corr_err[i,j] = data['one_point_corr_norm_stderr']
            noise_arr[i,j] = data['mean_noise_avg']
            density_arr[i,j] = data['mean_density_avg']
    for j in range(len(taus)-1):
        taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
        #axs[0][p].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
        axs[j][p].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color='blue', label=taulabel, marker='o',zorder=j)
        axs[j][p].axhline(y=0.0, color='black', linestyle='--')
        axs[j][0].set_ylabel(r'$\langle \delta |\xi| \delta \rho \rangle$')
        ax2 = axs[j][1].twinx()
        ax2.yaxis.set_ticklabels([])
        ax2.set_ylabel(taulabel)
    axs[-1][p].errorbar(lambdas, corr_arr[:,-1], yerr=2*corr_err[:,j], color='blue', label=r'$\tau_a=\infty$', marker='o')
    axs[-1][p].axhline(y=0.0, color='black', linestyle='--')
    axs[-1][0].set_ylabel(r'$\langle \delta |\xi| \delta \rho \rangle$')
    ax2 = axs[-1][1].twinx()
    ax2.yaxis.set_ticklabels([])
    ax2.set_ylabel(r'$\tau_a=\infty$')
    axs[0][p].set_title(r'$\phi=%.01f$' % phi)
    #axs[0][0].set_ylim([-0.0005,0.0005])
    axs[-1][p].set_xlabel(r'$\lambda_{\text{a}}$')

plt.savefig('plots/2d/density_cross_corr_norm_multipanel_alt.png')

fig, axs = plt.subplots(2,2,figsize=(6,4.5), sharex=True, sharey='row')
for p in range(len(phis)):
    phi = phis[p]
    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)
    for i in range(len(lambdas)):
        for j in range(len(taus)):
            tau = taus[j]
            Lambda = lambdas[i]
            if tau==float('inf'):
                thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir+'/density_noise_correlation_avg.npz')
            corr_arr[i,j] = data['one_point_corr_sparse_norm_avg']
            corr_err[i,j] = data['one_point_corr_sparse_norm_stderr']
            noise_arr[i,j] = data['mean_noise_avg']
            var_noise_arr[i,j] = data['var_noise_avg']
            print(var_noise_arr[i,j])
            density_arr[i,j] = data['mean_density_sparse_avg']
    for j in range(len(taus)-1):
        taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
        axs[0][p].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
        #axs[0][p].errorbar(lambdas, corr_arr[:,j]/np.max(np.abs(corr_arr[:,j])), yerr=2*corr_err[:,j]/np.max(np.abs(corr_arr[:,j])), color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
    axs[1][p].errorbar(lambdas, corr_arr[:,-1], yerr=2*corr_err[:,-1], color='blue', label=r'$\tau_a=\infty$', marker='o')
    axs[0][p].axhline(y=0.0, color='black', linestyle='--')
    axs[1][p].axhline(y=0.0, color='black', linestyle='--')
    axs[0][p].set_title(r'$\phi=%.01f$' % phi)
    axs[0][0].set_ylim([-0.005,0.0005])
    axs[0][1].legend(ncol=2, fontsize=8)#, loc='lower center')
    #axs[0][0].set_ylim([-0.0005,0.0005])
    axs[-1][1].legend()
    axs[-1][p].set_xlabel(r'$\lambda_{\text{a}}$')
    axs[1][0].set_ylabel(r'$\langle \delta |\xi| \delta \rho \rangle/\sigma_{|\xi|}\sigma_{\rho}$')
    axs[0][0].set_ylabel(r'$\langle \delta |\xi| \delta \rho \rangle/\sigma_{|\xi|}\sigma_{\rho}$')
plt.suptitle('Density-noise magnitude cross correlation')
plt.savefig('plots/2d/density_sparse_cross_corr_norm_multipanel.png')



#Alternative multipanel
fig, axs = plt.subplots(len(taus),2,figsize=(6,9), sharex=True, sharey='row')
for p in range(len(phis)):
    phi = phis[p]
    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)
    for i in range(len(lambdas)):
        for j in range(len(taus)):
            tau = taus[j]
            Lambda = lambdas[i]
            if tau==float('inf'):
                thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            else:
                thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir+'/density_noise_correlation_avg.npz')
            corr_arr[i,j] = data['one_point_corr_sparse_norm_avg']
            corr_err[i,j] = data['one_point_corr_sparse_norm_stderr']
            noise_arr[i,j] = data['mean_noise_avg']
            density_arr[i,j] = data['mean_density_sparse_avg']
    for j in range(len(taus)-1):
        taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
        #axs[0][p].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
        axs[j][p].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color='blue', label=taulabel, marker='o',zorder=j)
        axs[j][p].axhline(y=0.0, color='black', linestyle='--')
        axs[j][0].set_ylabel(r'$\langle \delta |\xi| \delta \rho \rangle$')
        ax2 = axs[j][1].twinx()
        ax2.yaxis.set_ticklabels([])
        ax2.set_ylabel(taulabel)
    axs[-1][p].errorbar(lambdas, corr_arr[:,-1], yerr=2*corr_err[:,j], color='blue', label=r'$\tau_a=\infty$', marker='o')
    axs[-1][p].axhline(y=0.0, color='black', linestyle='--')
    axs[-1][0].set_ylabel(r'$\langle \delta |\xi| \delta \rho \rangle$')
    ax2 = axs[-1][1].twinx()
    ax2.yaxis.set_ticklabels([])
    ax2.set_ylabel(r'$\tau_a=\infty$')
    axs[0][p].set_title(r'$\phi=%.01f$' % phi)
    #axs[0][0].set_ylim([-0.0005,0.0005])
    axs[-1][p].set_xlabel(r'$\lambda_{\text{a}}$')

plt.savefig('plots/2d/density_sparse_cross_corr_norm_multipanel_alt.png')