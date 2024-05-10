import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

kT=0.0
va=1.0
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]
Nx=96
Ny=112
nx=200
ny=200
interpolation='linear'
compressibility='compressible'
cov_type='exponential'

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/fene/2d/kT=%f/va=%f' % (kT, va)

#Collect correlation measurements
corr_arr = np.zeros((len(lambdas),len(taus)))
corr_err = np.zeros((len(lambdas),len(taus)))
noise_arr = np.zeros((len(lambdas),len(taus)))
pressure_arr = np.zeros((len(lambdas),len(taus)))
for i in range(len(lambdas)):
    for j in range(len(taus)):
        tau = taus[j]
        Lambda = lambdas[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        data = np.load(thedir+'/pressure_noise_correlation_avg.npz')
        corr_arr[i,j] = data['one_point_corr_abs_avg']
        corr_err[i,j] = data['one_point_corr_abs_stderr']
        noise_arr[i,j] = data['mean_noise_avg']
        pressure_arr[i,j] = data['mean_pressure_avg']


mymax = np.max(np.abs(corr_arr))
fig = plt.figure()
for i in range(len(lambdas)):
    for j in range(len(taus)):
        plt.scatter(lambdas[i], taus[j], c=corr_arr[i,j],cmap='RdBu_r',vmin=-mymax, vmax=mymax,linewidth=1, edgecolors='black', s=100)
plt.xlabel(r'$\lambda_{\text{a}}$')
plt.ylabel(r'$\tau_{\text{a}}$')
plt.yscale('log')
#plt.gca().set_aspect('equal')
plt.savefig('plots/2d/pressure_cross_corr_2d.png')

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
plt.xlabel(r'$\lambda_{\text{a}}$')
plt.ylabel(r'$\langle \delta |\mathbf{\xi}| \delta |p| \rangle$')
plt.legend(loc='lower left', fontsize=9)
#plt.yscale('log')
#plt.gca().set_aspect('equal')
plt.savefig('plots/2d/pressure_cross_corr.png')

fig, axs = plt.subplots(2,1,figsize=(3,4.5), sharex=True, sharey='row')
basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/fene/2d/kT=%f/va=%f' % (kT, va)
for i in range(len(lambdas)):
    for j in range(len(taus)):
        tau = taus[j]
        Lambda = lambdas[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        data = np.load(thedir+'/pressure_noise_correlation_avg.npz')
        corr_arr[i,j] = data['one_point_corr_norm_avg']
        corr_err[i,j] = data['one_point_corr_norm_stderr']
        noise_arr[i,j] = data['mean_noise_avg']
        pressure_arr[i,j] = data['mean_pressure_avg']
for j in range(len(taus)-1):
    taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
    axs[0].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
    #axs[0][p].errorbar(lambdas, corr_arr[:,j]/np.max(np.abs(corr_arr[:,j])), yerr=2*corr_err[:,j]/np.max(np.abs(corr_arr[:,j])), color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
axs[1].errorbar(lambdas, corr_arr[:,-1], yerr=2*corr_err[:,j], color='blue', label=r'$\tau_a=\infty$', marker='o')
axs[0].axhline(y=0.0, color='black', linestyle='--')
axs[1].axhline(y=0.0, color='black', linestyle='--')
axs[0].legend(ncol=2, fontsize=8)#, loc='lower center')
#axs[0][0].set_ylim([-0.0005,0.0005])
axs[-1].legend()
axs[-1].set_xlabel(r'$\lambda_{\text{a}}$')
axs[1].set_ylabel(r'$\langle \delta |\xi| \delta p \rangle/\sigma_{|\xi|}\sigma_{p}$')
axs[0].set_ylabel(r'$\langle \delta |\xi| \delta p \rangle/\sigma_{|\xi|}\sigma_{p}$')
axs[0].set_ylim([-0.06,0.005])
plt.suptitle('Pressure-noise magnitude cross correlation')
plt.savefig('plots/2d/pressure_cross_corr_norm_multipanel.png')


#Alternative multipanel
fig, axs = plt.subplots(len(taus),1,figsize=(3,9), sharex=True, sharey='row')
basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/fene/2d/kT=%f/va=%f' % (kT, va)
for i in range(len(lambdas)):
    for j in range(len(taus)):
        tau = taus[j]
        Lambda = lambdas[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        data = np.load(thedir+'/pressure_noise_correlation_avg.npz')
        corr_arr[i,j] = data['one_point_corr_norm_avg']
        corr_err[i,j] = data['one_point_corr_norm_stderr']
        noise_arr[i,j] = data['mean_noise_avg']
        pressure_arr[i,j] = data['mean_pressure_avg']
for j in range(len(taus)-1):
    taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
    #axs[0][p].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
    axs[j].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color='blue', label=taulabel, marker='o',zorder=j)
    axs[j].axhline(y=0.0, color='black', linestyle='--')
    axs[j].set_ylabel(r'$\langle \delta |\xi| \delta p \rangle$')
    ax2 = axs[j].twinx()
    ax2.yaxis.set_ticklabels([])
    ax2.set_ylabel(taulabel)
axs[-1].errorbar(lambdas, corr_arr[:,-1], yerr=2*corr_err[:,j], color='blue', label=r'$\tau_a=\infty$', marker='o')
axs[-1].axhline(y=0.0, color='black', linestyle='--')
axs[-1].set_ylabel(r'$\langle \delta |\xi| \delta p \rangle$')
ax2 = axs[-1].twinx()
ax2.yaxis.set_ticklabels([])
ax2.set_ylabel(r'$\tau_a=\infty$')
#axs[0][0].set_ylim([-0.0005,0.0005])
axs[-1].set_xlabel(r'$\lambda_{\text{a}}$')

plt.savefig('plots/2d/pressure_cross_corr_norm_multipanel_alt.png')

#Using absolute value of pressure

fig, axs = plt.subplots(2,1,figsize=(3,4.5), sharex=True, sharey='row')
basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/fene/2d/kT=%f/va=%f' % (kT, va)
for i in range(len(lambdas)):
    for j in range(len(taus)):
        tau = taus[j]
        Lambda = lambdas[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        data = np.load(thedir+'/pressure_noise_correlation_avg.npz')
        corr_arr[i,j] = data['one_point_corr_abs_norm_avg']
        corr_err[i,j] = data['one_point_corr_abs_norm_stderr']
        noise_arr[i,j] = data['mean_noise_avg']
        pressure_arr[i,j] = data['mean_pressure_avg']
for j in range(len(taus)-1):
    taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
    if taus[j]==float('inf'):
        taulabel=r'$\tau_a=\infty$'
    axs[0].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
    #axs[0][p].errorbar(lambdas, corr_arr[:,j]/np.max(np.abs(corr_arr[:,j])), yerr=2*corr_err[:,j]/np.max(np.abs(corr_arr[:,j])), color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
axs[1].errorbar(lambdas, corr_arr[:,-1], yerr=2*corr_err[:,j], color='blue', label=r'$\tau_a=\infty$', marker='o')
axs[0].axhline(y=0.0, color='black', linestyle='--')
axs[1].axhline(y=0.0, color='black', linestyle='--')
axs[0].legend(ncol=2, fontsize=8)#, loc='lower center')
#axs[0][0].set_ylim([-0.0005,0.0005])
axs[-1].legend()
axs[-1].set_xlabel(r'$\lambda_{\text{a}}$')
axs[1].set_ylabel(r'$\langle \delta |\xi| \delta |p| \rangle/\sigma_{|\xi|}\sigma_{|p|}$')
axs[0].set_ylabel(r'$\langle \delta |\xi| \delta |p| \rangle/\sigma_{|\xi|}\sigma_{|p|}$')
plt.suptitle('Pressure magnitude-noise magnitude cross correlation')
plt.savefig('plots/2d/pressure_abs_cross_corr_norm_multipanel.png')


#Alternative multipanel
fig, axs = plt.subplots(len(taus),1,figsize=(3,9), sharex=True, sharey='row')
basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/fene/2d/kT=%f/va=%f' % (kT, va)
for i in range(len(lambdas)):
    for j in range(len(taus)):
        tau = taus[j]
        Lambda = lambdas[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        data = np.load(thedir+'/pressure_noise_correlation_avg.npz')
        corr_arr[i,j] = data['one_point_corr_abs_norm_avg']
        corr_err[i,j] = data['one_point_corr_abs_norm_stderr']
        noise_arr[i,j] = data['mean_noise_avg']
        pressure_arr[i,j] = data['mean_pressure_avg']
for j in range(len(taus)-1):
    taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
    #axs[0][p].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color=colors_tau[j], label=taulabel, marker='o',zorder=j, alpha=0.5)
    axs[j].errorbar(lambdas, corr_arr[:,j], yerr=2*corr_err[:,j], color='blue', label=taulabel, marker='o',zorder=j)
    axs[j].axhline(y=0.0, color='black', linestyle='--')
    axs[j].set_ylabel(r'$\langle \delta |\xi| \delta |p| \rangle$')
    ax2 = axs[j].twinx()
    ax2.yaxis.set_ticklabels([])
    ax2.set_ylabel(taulabel)
axs[-1].errorbar(lambdas, corr_arr[:,-1], yerr=2*corr_err[:,j], color='blue', label=r'$\tau_a=\infty$', marker='o')
axs[-1].axhline(y=0.0, color='black', linestyle='--')
axs[-1].set_ylabel(r'$\langle \delta |\xi| \delta |p| \rangle$')
ax2 = axs[-1].twinx()
ax2.yaxis.set_ticklabels([])
ax2.set_ylabel(r'$\tau_a=\infty$')
#axs[0][0].set_ylim([-0.0005,0.0005])
axs[-1].set_xlabel(r'$\lambda_{\text{a}}$')

plt.savefig('plots/2d/pressure_abs_cross_corr_norm_multipanel_alt.png')