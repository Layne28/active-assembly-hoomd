'''
Plot noise time and space correlations
Created June 27, 2024
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import scipy
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import AnalysisTools.trajectory_stats as stats

def main():

    tau=10.0
    Lambda=5.0

    tmax=200.0

    nx=400
    ny=400
    compressibility='incompressible'
    cov_type='exponential'
    
    colorscheme='viridis'
    if compressibility=='incompressible':
        colorscheme='RdBu_r'

    #Load data
    basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/noise/2d'
    thedir = basedir + '/tau=%f/lambda=%f/nx=%d_ny=%d/%s/%s/' % (tau, Lambda, nx, ny, compressibility, cov_type)
    noise_data = np.load(thedir + 'seed=1/noise_stats.npz')
    
    print(noise_data['tcorr'])

    times = noise_data['tcorr'][:,0]
    tcorr = noise_data['tcorr'][:,1]
    rcorr = noise_data['rcorr']
    spacing = noise_data['rspacing']
    rvals = noise_data['rvals']
    radial_corr = noise_data['radial_corr']
    radial_vals = noise_data['radial_vals']
    
    x = np.linspace(0,rcorr.shape[0]*spacing[0], rcorr.shape[0])
    y = np.linspace(0,rcorr.shape[1]*spacing[1], rcorr.shape[1])
    
    xv, yv = np.meshgrid(x,y)
    print(xv, yv)
    
    print(times)
    print(tcorr)
    print(np.max(rcorr))

    #Make plots
    fig, axs = plt.subplots(1,1)
    
    axs.plot(times, np.exp(-times/tau), color='red', label='theory')
    axs.scatter(times,tcorr/tcorr[0], c='blue', s=2, label='simulation')
    #axs.fill_between(times, msdavg+2*msderr, msdavg-2*msderr, alpha=0.4, color='blue', edgecolor='none')

    axs.set_xlabel(r'$t$')
    axs.set_ylabel(r'$C(t)$')
    axs.legend()#loc='upper right')
    
    plt.savefig('plots/2d/noise_tcorr_%s_tau=%.01f_lambda=%.01f_nx=%d_ny=%d.png' % (compressibility, tau, Lambda, nx, ny), dpi=600, bbox_inches='tight')
    plt.close()
    
    #space corr
    fig, axs = plt.subplots(1,2)
    
    print('min value:', np.min(rcorr/np.max(rcorr)))
    
    #axs.plot(times, np.exp(-times/tau), color='red', label='theory')
    #axs.scatter(times,tcorr, c='blue', s=2, label='simulation')
    axs[0].imshow(rcorr/np.max(rcorr), origin='lower', extent=(0,rcorr.shape[0]*spacing[0],0,rcorr.shape[1]*spacing[1]), cmap=colorscheme, vmin=0,vmax=1)
    axs[0].set_xlim([0,20])
    axs[0].set_ylim([0,20])
    axs[0].set_title('simulation')
    axs[1].imshow(np.exp(-(np.sqrt(xv**2+yv**2))/Lambda), origin='lower', extent=(0,rcorr.shape[0]*spacing[0],0,rcorr.shape[1]*spacing[1]), cmap=colorscheme, vmin=0,vmax=1)
    axs[1].set_xlim([0,20])
    axs[1].set_ylim([0,20])
    axs[1].set_title('theory')
    #axs.fill_between(times, msdavg+2*msderr, msdavg-2*msderr, alpha=0.4, color='blue', edgecolor='none')

    #axs.set_xlabel(r'$t$')
    #axs.set_ylabel(r'$C(t)$')
    #axs.legend()#loc='upper right')
    
    plt.savefig('plots/2d/noise_rcorr_%s_tau=%.01f_lambda=%.01f_nx=%d_ny=%d.png' % (compressibility, tau, Lambda, nx, ny), dpi=600, bbox_inches='tight')
    plt.close()
    
    #radial corr
    fig, axs = plt.subplots(1,1)
    
    axs.plot(rvals, np.exp(-rvals/Lambda), color='red', label='theory')
    axs.scatter(rvals.flatten(),rcorr.flatten()/rcorr[0,0], c='green', s=6, label='simulation')
    axs.scatter(radial_vals,radial_corr/radial_corr[0], c='blue', s=4, label='simulation')
    #axs.fill_between(times, msdavg+2*msderr, msdavg-2*msderr, alpha=0.4, color='blue', edgecolor='none')

    axs.set_xlabel(r'$r$')
    axs.set_ylabel(r'$C(r)$')
    #axs.legend()#loc='upper right')
    
    axs.set_xlim([0,50])
    axs.set_ylim([-0.1,1])
    
    plt.savefig('plots/2d/noise_radcorr_%s_tau=%.01f_lambda=%.01f_nx=%d_ny=%d.png' % (compressibility, tau, Lambda, nx, ny), dpi=600, bbox_inches='tight')
    plt.close()

main()