'''
Compute AOUP fit to MSD and plot vs data
Use AnalysisTools fit_aoup function
Created June 19, 2024
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import scipy
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import AnalysisTools.msd as msd
import AnalysisTools.trajectory_stats as stats

def main():

    kT=0.0
    phi=0.0
    va=1.0
    taus = [0.1, 1.0, 10.0, 100.0]
    Lambdas = [1.0, 3.0, 5.0, 10.0, 20.0]

    lambda_mat = np.zeros((len(taus), len(Lambdas)))
    tau_mat = np.zeros((len(taus), len(Lambdas)))
    D_mat = np.zeros((len(taus), len(Lambdas)))
    tau_p_mat = np.zeros((len(taus), len(Lambdas)))

    numstring='all'
    tmax=200.0
    nchunks=1

    Lx=200.000000
    Ly=200.000000
    nx=400
    ny=400
    interpolation='linear'
    compressibility='compressible'
    cov_type='exponential'
    potential='none'

    #colors = mpl.cm.plasma(np.linspace(0,1,nchunks))

    #Load data
    for i in range(len(taus)):
        for j in range(len(Lambdas)):
            tau = taus[i]
            Lambda = Lambdas[j]
            tau_mat[i][j] = tau
            lambda_mat[i][j] = Lambda
            basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)
            thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            msd_data = np.load(thedir + '/msd_tmax=%f_nchunks=%d_%s_avg.npz' % (tmax, nchunks, numstring))

            msdavg = msd_data['msd_0_avg']
            msderr = msd_data['msd_0_stderr']
            times = msd_data['times_avg']

            #Get fit
            aoup_fit_params = msd.fit_aoup(times, msdavg, 2)
            D_mat[i][j] = aoup_fit_params[0]
            tau_p_mat[i][j] = aoup_fit_params[1]#[1]

    #Save fit data
    fit_dict = {}
    fit_dict['lambda_mat'] = lambda_mat
    fit_dict['tau_mat'] = tau_mat
    fit_dict['D_mat'] = D_mat
    fit_dict['tau_p_mat'] = tau_p_mat
    outfile = basedir + '/msd_aoup_fit_Lx=%f_Ly=%f_nx=%d_ny=%d_interpolation=%s_%s_%s.npz' % (Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
    np.savez(outfile, **fit_dict)

    #Make plot
    figsize = plt.rcParams.get('figure.figsize')
    figsize[0] *= 2
    figsize[1] *= 2
    fig, axs = plt.subplots(len(taus),len(Lambdas), sharex=True, sharey=True, figsize=figsize)

    for i in range(len(taus)):
        for j in range(len(Lambdas)):
            tau = taus[i]
            Lambda = Lambdas[j]
            basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)
            thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            msd_data = np.load(thedir + '/msd_tmax=%f_nchunks=%d_%s_avg.npz' % (tmax, nchunks, numstring))

            msdavg = msd_data['msd_0_avg']
            msderr = msd_data['msd_0_stderr']
            times = msd_data['times_avg']

            #data
            axs[i][j].scatter(times,msdavg, c='blue', s=0.5, label='data')
            axs[i][j].fill_between(times, msdavg+2*msderr, msdavg-2*msderr, alpha=0.4, color='blue', edgecolor='none')

            #fit
            print('Lambda: %f tau: %f D: %f tau_p: %f' % (Lambda, tau, D_mat[i][j], tau_p_mat[i][j]))
            v_aoup_msd = np.vectorize(msd.aoup_msd_func(2))
            axs[i][j].plot(times, v_aoup_msd(times, D_mat[i][j], tau_p_mat[i][j]), color='red', label='fit', linewidth=1.0)

            #t and t^2 to guide the eye
            #axs[i][j].plot(times, times, color='black', linestyle='--', label=r'$t$')
            #axs[i][j].plot(times, 30*times**2, color='gray', linestyle=':', label=r'$t^2$')

            axs[i][j].set_xscale('log')
            axs[i][j].set_yscale('log')


            if i==len(taus)-1:
                axs[i][j].set_xlabel(r'$t$')

            if j==0:
                axs[i][j].set_ylabel(r'MSD')

            if i==0:
                axs[i][j].set_title(r'$\lambda_{\text{a}}=%.01f$ ' % Lambda)

            if j==len(Lambdas)-1:
                ax2 = axs[i][j].twinx()
                ax2.get_yaxis().set_ticks([])
                ax2.set_ylabel(r'$\tau_{\text{a}}=%.01f$' % tau)

    axs[0][0].legend(fontsize=8)#loc='upper right') 

    plt.savefig('plots/2d/msd_fit_%s_%s_phi=%.01f_va=%.01f_Lx=%.01f_Ly=%.01f.png' % (potential, compressibility, phi, va, Lx, Ly), dpi=600, bbox_inches='tight')
    plt.close()

main()