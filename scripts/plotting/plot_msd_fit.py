'''
Compute AOUP fit to MSD and plot vs data
Created June 18, 2024
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import scipy

import AnalysisTools.msd as msd
import AnalysisTools.trajectory_stats as stats

def main():

    kT=0.0
    phi=0.0
    va=1.0
    tau=10.0
    Lambda=10.0

    numstring='all'
    tmax=200.0
    nchunks=1

    #taus = [0.1, 1.0, 10.0, float('inf')]
    #lambdas = [1.0, 3.0, 10.0, 30.0]
    #phis = [0.1]#,0.4]
    #taus = [0.1, 1.0, 10.0, 100.0]#, float('inf')]
    #lambdas = [0.0, 1.0, 3.0, 5.0, 10.0, 20.0]

    Lx=200.000000
    Ly=200.000000
    nx=400
    ny=400
    interpolation='linear'
    compressibility='compressible'
    cov_type='exponential'
    potential='none'

    colors = mpl.cm.plasma(np.linspace(0,1,nchunks))

    #Load data
    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)
    thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
    msd_data = np.load(thedir + '/msd_tmax=%f_nchunks=%d_%s_avg.npz' % (tmax, nchunks, numstring))

    msdavg = msd_data['msd_0_avg']
    msderr = msd_data['msd_0_stderr']
    times = msd_data['times_avg']

    #Get fit
    aoup_fit_params, pcov = scipy.optimize.curve_fit(aoup_msd_2d_loglog, np.log(times[1:]), np.log(msdavg[1:]))

    print(aoup_fit_params)
    D = aoup_fit_params[0]
    tau_p = aoup_fit_params[1]#[1]

    #Make plot
    fig, axs = plt.subplots(1,1)

    #data
    axs.scatter(times,msdavg, c='blue', s=5)
    #axs.fill_between(times, msdavg+2*msderr, msdavg-2*msderr, alpha=0.4, color=colors[i])

    #fit
    v_aoup_msd = np.vectorize(aoup_msd_2d)
    #axs.plot(times, v_aoup_msd(times, D, tau_p), color='red')
    axs.plot(times, v_aoup_msd(times, D, tau_p), color='red')

    #t and t^2 to guide the eye
    #axs.plot(times, times, color='black', linestyle='--', label=r'$t$')
    #axs.plot(times, 30*times**2, color='gray', linestyle=':', label=r'$t^2$')


    axs.set_xlabel(r'$t$')
    axs.set_ylabel(r'MSD')

    axs.legend()#loc='upper right')

    #plt.xlim([0,myxmax])
    #axs.set_ylim([10**(-2),3.0])
    axs.set_xscale('log')
    axs.set_yscale('log')

    plt.savefig('plots/2d/msd_fit_%s_phi=%.01f_va=%.01f_tau=%.01f_lambda=%.01f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, tau, Lambda, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()

def aoup_msd(t, D, tau, d):

    return 2*d*D * (t + tau*(np.exp(-t/tau) - 1))

def aoup_msd_2d(t, D, tau):

    return aoup_msd(t,D,tau,2)

def aoup_msd_2d_loglog(t, D, tau):

    return np.log(aoup_msd(np.exp(t),D,tau,2))

main()