import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.cluster as cluster
import AnalysisTools.trajectory_stats as stats

kT=0.0
phi=0.1
va=1.0
#taus = [0.1, 1.0, 10.0, float('inf')]
#lambdas = [1.0, 3.0, 10.0, 30.0]
phis = [0.1,0.4]
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]
#lambdas = [1.0, 3.0, 10.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'
potential='none'

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))
colors = mpl.cm.viridis(np.linspace(0,1,len(lambdas)))

for phi in phis:

    #print(phi)
    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/%s/2d/kT=%f/phi=%f/va=%f' % (potential, kT, phi, va)

    #fig, axs = plt.subplots(len(lambdas),1,figsize=(3.0,7.0), sharex=True)
    fig, axs = plt.subplots(1,1)
    for j in range(len(lambdas)):
        Lambda = lambdas[j]
        ls = []
        for i in range(len(taus)-1):
            tau = taus[i]
            #print(Lambda, tau)
            thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir + '/csd_rc=1.500000.npz')
            #print(list(data))
            #print('loaded data')
            histavg = data['hist_nlast']
            #histerr = data['hist_nlast_stderr']
            bins = data['bins']
            ls.append(cluster.get_avg_size(bins, histavg))
            #print('appended')
        taulabel = r'$\tau_a=%.01f$' % taus[i]
        axs.plot(taus[:-1], ls, marker='o', markersize=5, color=colors[j], label=r'$\lambda_a=%.01f$' % lambdas[j])
        #print('plotted')
    axs.set_xscale('log')
    #axs[j].set_xlabel(r'$\tau_a$')
    axs.set_ylabel(r'$\langle n \rangle$')
    axs.legend(fontsize=8, loc='upper left')
    axs.set_xlabel(r'$\tau_a$')
    plt.savefig('plots/2d/cluster_avg_%s_vary_tau_phi=%f_va=%f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()

    fig, axs = plt.subplots(1,1)
    for j in range(len(lambdas)):
        Lambda = lambdas[j]
        ls = []
        for i in range(len(taus)-1):
            tau = taus[i]
            thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
            data = np.load(thedir + '/csd_rc=1.500000.npz')
            #print(list(data))
            histavg = data['hist_nlast']
            #histerr = data['hist_nlast_stderr']
            bins = data['bins']
            ls.append(cluster.get_avg_mass_weighted_size(bins, histavg))
        taulabel = r'$\tau_a=%.01f$' % taus[i]
        axs.plot(taus[:-1], ls, marker='o', markersize=5, color=colors[j], label=r'$\lambda_a=%.01f$' % lambdas[j])
    axs.set_xscale('log')
    #axs[j].set_xlabel(r'$\tau_a$')
    axs.set_ylabel(r'$\langle n^2 \rangle/\langle n \rangle$')
    axs.legend(fontsize=8, loc='upper left')
    axs.set_xlabel(r'$\tau_a$')
    plt.savefig('plots/2d/cluster_mw_avg_%s_vary_tau_phi=%f_va=%f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()

    #Quenched case
    fig, axs = plt.subplots(1,1)
    ls = []
    for i in range(len(lambdas)):
        Lambda = lambdas[i]
        thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        data = np.load(thedir + '/csd_rc=1.500000.npz')
        histavg = data['hist_nlast']
        #histerr = data['hist_nlast_stderr']
        bins = data['bins']
        ls.append(cluster.get_avg_size(bins, histavg))

    axs.plot(lambdas, ls, marker='o', markersize=10)
    axs.set_xlabel(r'$\lambda_a$')
    axs.set_ylabel(r'$\langle n \rangle$')

    plt.savefig('plots/2d/cluster_avg_%s_quenched_vary_lambda_phi=%.01f_va=%.01f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()

    fig, axs = plt.subplots(1,1)
    ls = []
    for i in range(len(lambdas)):
        Lambda = lambdas[i]
        thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        data = np.load(thedir + '/csd_rc=1.500000.npz')
        histavg = data['hist_nlast']
        #histerr = data['hist_nlast_stderr']
        bins = data['bins']
        ls.append(cluster.get_avg_mass_weighted_size(bins, histavg))

    axs.plot(lambdas, ls, marker='o', markersize=10)
    axs.set_xlabel(r'$\lambda_a$')
    axs.set_ylabel(r'$\langle n^2 \rangle/\langle n \rangle$')

    plt.savefig('plots/2d/cluster_mw_avg_%s_quenched_vary_lambda_phi=%.01f_va=%.01f_Lx=%.01f_Ly=%.01f.png' % (potential, phi, va, Lx, Ly), dpi=300, bbox_inches='tight')
    plt.close()
