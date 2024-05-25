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
potential='fene'

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/va=%f' % (potential, kT, va)

colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))


#Collect correlation measurements

#corr_abs_arr[i,j] = data['spatial_corr_abs_norm_avg']
#corr_abs_err[i,j] = data['one_point_corr_abs_norm_stderr']

fig, axs = plt.subplots(len(lambdas),2,figsize=(6.0,7.0))
for i in range(len(lambdas)):
    for j in range(len(taus)):
        tau = taus[j]
        Lambda = lambdas[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)

        taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
        if taus[j]==float('inf'):
            taulabel=r'$\tau_a=\infty$'

        data = np.load(thedir+'/pressure_noise_correlation_spatial_avg.npz')
        #if 'spatial_corr_norm_avg' in data.keys():
        dist_arr = data['spatial_corr_avg'][:,0] #data output got messed up so use these (accidentally "normalized" the x values in norm_avg)
        corr_arr = data['spatial_corr_norm_reverse_avg'][:,1]
        corr_err = data['spatial_corr_norm_reverse_stderr'][:,1]

        #print(corr_arr)
        print(Lambda, tau)
        print(corr_err)

        #axs[i].errorbar(dist_arr, np.abs(corr_arr), yerr=2*corr_err, color=colors_tau[j], label=taulabel,zorder=j, alpha=0.5)
        axs[i][0].plot(dist_arr, corr_arr, color=colors_tau[j], label=taulabel,zorder=j, alpha=0.5, linewidth=0.5)
        axs[i][1].plot(dist_arr, corr_arr, color=colors_tau[j], label=taulabel,zorder=j, alpha=0.5, linewidth=0.5)
        axs[i][0].fill_between(dist_arr, corr_arr-2*corr_err, corr_arr+2*corr_err, alpha=0.2, color=colors_tau[j], linewidth=0)
        axs[i][1].fill_between(dist_arr, corr_arr-2*corr_err, corr_arr+2*corr_err, alpha=0.2, color=colors_tau[j], linewidth=0)


        axs[i][0].axhline(y=0.0, color='black', linestyle='--')
        axs[i][1].axhline(y=0.0, color='black', linestyle='--')
        #axs[i].set_ylabel(r'$\langle \delta |\xi|(0) \delta p(r) \rangle/\sigma_{|\xi|}\sigma_{p}$')
        axs[i][0].set_ylabel(r'$\langle \delta |\xi|(0) \delta p(r) \rangle$')
        axs[i][0].set_title(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
        axs[0][0].legend(ncol=2, fontsize=8)#, loc='lower center')
        axs[i][0].set_xlim([0,5])
        axs[i][1].set_xlim([5,30])
        axs[i][1].set_ylim([-0.5,0.5])
        axs[i][0].set_ylim([-4,4])
        #axs[i].set_ylim([10**(-3),5.0])
        #axs[i].set_yscale('log')
        #axs[i].set_xscale('log')
        #axs[i].set_yscale('log')

axs[-1][0].set_xlabel(r'$r$')
axs[-1][1].set_xlabel(r'$r$')

plt.suptitle('Pressure-noise magnitude cross correlation')
plt.savefig('plots/2d/pressure_spatial_cross_corr_reverse_%s.png' % potential)

#Absolute value of pressure
fig, axs = plt.subplots(len(lambdas),2,figsize=(6.0,7.0))#, sharey=True)
for i in range(len(lambdas)):
    for j in range(len(taus)):
        tau = taus[j]
        Lambda = lambdas[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Nx=%d_Ny=%d/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Nx, Ny, nx, ny, interpolation, compressibility, cov_type)

        taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
        if taus[j]==float('inf'):
            taulabel=r'$\tau_a=\infty$'

        data = np.load(thedir+'/pressure_noise_correlation_spatial_avg.npz')
        if 'spatial_corr_norm_reverse_avg' in data.keys():
            dist_arr = data['spatial_corr_avg'][:,0] #data output got messed up so use these (accidentally "normalized" the x values in norm_avg)
            corr_arr = data['spatial_corr_abs_norm_reverse_avg'][:,1]
            corr_err = data['spatial_corr_abs_norm_reverse_stderr'][:,1]

            #print(corr_arr)

            #axs[i].errorbar(dist_arr, np.abs(corr_arr), yerr=2*corr_err, color=colors_tau[j], label=taulabel,zorder=j, alpha=0.5)
            #axs[i].plot(dist_arr, corr_arr, color=colors_tau[j], label=taulabel,zorder=j, alpha=0.5)
            axs[i][0].plot(dist_arr, corr_arr, color=colors_tau[j], label=taulabel,zorder=j, alpha=0.5, linewidth=0.5)
            axs[i][1].plot(dist_arr, corr_arr, color=colors_tau[j], label=taulabel,zorder=j, alpha=0.5, linewidth=0.5)
            axs[i][0].fill_between(dist_arr, corr_arr-2*corr_err, corr_arr+2*corr_err, alpha=0.2, color=colors_tau[j], linewidth=0)
            axs[i][1].fill_between(dist_arr, corr_arr-2*corr_err, corr_arr+2*corr_err, alpha=0.2, color=colors_tau[j], linewidth=0)

        axs[i][0].axhline(y=0.0, color='black', linestyle='--')
        axs[i][1].axhline(y=0.0, color='black', linestyle='--')
        #axs[i].set_ylabel(r'$\langle \delta |\xi|(0) \delta |p|(r) \rangle/\sigma_{|\xi|}\sigma_{|p|}$')
        axs[i][0].set_ylabel(r'$\langle \delta |p|(0) \delta |\xi|(r) \rangle$')
        axs[i][0].set_title(r'$\lambda_{\text{a}}=%.01f$' % Lambda)
        axs[0][1].legend(ncol=2,fontsize=8)#, loc='lower center')
        #axs[i][0].set_xlim([0,5])
        #axs[i][0].set_ylim([-3,5])
        axs[i][1].set_xlim([5,30])
        axs[i][1].set_ylim([-0.05,0.5])
        #axs[i].set_ylim([10**(-3),5.0])
        #axs[i].set_yscale('log')
        #axs[i].set_xscale('log')
        #axs[i].set_yscale('log')

axs[-1][0].set_xlabel(r'$r$')
axs[-1][1].set_xlabel(r'$r$')

plt.suptitle('Pressure magnitude-noise magnitude cross correlation')
plt.savefig('plots/2d/pressure_abs_spatial_cross_corr_reverse_%s.png' % potential)