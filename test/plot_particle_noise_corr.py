'''
Figure: Noise-density correlation

Makes a figure showing the average noise conditioned on a particle being present
'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec

import AnalysisTools.particle_io as io

avg_speed = np.sqrt(np.pi/2.0) #average speed in 2d for va=1
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0, 20.0]
phis=[0.1,0.4]
types = ['wca', 'none']

colors_tau = mpl.cm.viridis(np.linspace(0,1,len(taus)))

legend_fontsize=6
title_fontsize=10

#Collect correlation measurements
diff_arr = np.zeros((len(lambdas),len(taus)))
diff_err = np.zeros((len(lambdas),len(taus)))

figsize = plt.rcParams.get('figure.figsize')
figsize[1] *= 1.5

#########################################

fig = plt.figure(figsize=figsize)
gs = GridSpec(2,3,figure=fig, height_ratios=[1,1], wspace=0.2, hspace=0.7)

ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[0,1])
ax3 = fig.add_subplot(gs[0,2])

ax1b = fig.add_subplot(gs[1,0])
ax2b = fig.add_subplot(gs[1,1])
ax3b = fig.add_subplot(gs[1,2])

axs = [ax1,ax2,ax3]
config_axs = [ax1b, ax2b, ax3b]

for i in range(1,3):
    axs[i].sharey(axs[0])
    plt.setp(axs[i].get_yticklabels(), visible=False)
    axs[i].tick_params(axis='y', which='both', left=False)


#fig, axs = plt.subplots(2,3, sharex=True, sharey=True, figsize=figsize)

plt.subplots_adjust(wspace=0.07,hspace=0.3)
for p in range(len(phis)):
    phi = phis[p]
    for t in types:
        if not (t=='none' and p==1):
            if t=='wca':
                mystyle='solid'
                mymarker='o'
                index=p
            else:
                mystyle='solid'#'dashed'
                mymarker='o'#'s'
                index=2
            for i in range(len(lambdas)):
                for j in range(len(taus)):
                    tau = taus[j]
                    Lambda = lambdas[i]
                    if tau==float('inf'):
                        myfile = 'data/fig4/density_noise_corr_%s_phi=%.1f_quenched_lambda=%.0f.npz' % (t, phi, Lambda)
                    else:
                        myfile = 'data/fig4/density_noise_corr_%s_phi=%.1f_tau=%.01f_lambda=%.0f.npz' % (t, phi, tau, Lambda)
                    data = np.load(myfile)
                    diff_arr[i,j] = data['noise_mag_conditional_diff_avg']
                    diff_err[i,j] = data['noise_mag_conditional_diff_stderr']
            for j in range(len(taus)):
                taulabel = r'$\tau_{\text{a}}=%.01f$' % taus[j]
                if taus[j]==float('inf'):
                    taulabel=r'$\tau_{\text{a}}=\infty$'
                axs[index].errorbar(lambdas, diff_arr[:,j], yerr=2*diff_err[:,j], color=colors_tau[j], label=taulabel, marker=mymarker, markersize=5.0, zorder=j, linestyle=mystyle)
            axs[index].axhline(y=0.0, color='black', linestyle='--')
            axs[index].axhline(y=-avg_speed, color='gray', linestyle='dotted')
            axs[index].set_xlim([0,20.8])
            axs[index].xaxis.set_ticks([1,5,10,20])
            axs[0].set_ylabel(r'$\Delta \langle |\xi|\rangle$')
            
            #ax2 = axs[index][1].twinx()
            #if t=='wca':
            #    ax2.set_ylabel('WCA')
            #else:
            #    ax2.set_ylabel('non-interacting')
            #ax2.yaxis.set_major_locator(ticker.NullLocator())
        axs[index].set_xlabel(r'$\lambda_{\text{a}}$')
        if index<2:
            axs[index].set_title(r'WCA, $\phi=%.01f$' % phi, fontsize=title_fontsize)
        else:
            axs[index].set_title(r'non-interacting', fontsize=title_fontsize)

    axs[1].legend(fontsize=legend_fontsize, loc='lower left')
    

config_taus = [float('inf'), 0.1, float('inf')]
config_lambdas = [1, 20, 20]
phis = [0.1, 0.4, 0.0]
indices=[-1,0,-1]
for i in range(len(config_axs)):
    ax = config_axs[i]
    tau = config_taus[i]
    Lambda = config_lambdas[i]
    
    if tau==float('inf'):
        taustr='quenched'
    else:
        taustr='tau=%.01f' % tau
    
    #Noise fields
    srate = 1
    pointsize=2.0
    maxlim=50
    buffer=0.1
    data = io.load_noise_traj('data/noise_particle_corr/noise_%s_lambda=%.0f.h5' % (taustr, Lambda))

    if i==1:
        print(data['times'])
    Lx = data['ncells'][0]*data['spacing'][0]
    Ly = data['ncells'][1]*data['spacing'][1]
    #xvals = np.arange(data['ncells'][0])*data['spacing'][0]-Lx/2.0
    #yvals = np.arange(data['ncells'][1])*data['spacing'][1]-Ly/2.0
    xvals, yvals = np.meshgrid(np.linspace(0,data['ncells'][0]*data['spacing'][0],data['ncells'][0])-Lx/2.0,
    np.linspace(0,data['ncells'][1]*data['spacing'][1],data['ncells'][1])-Ly/2.0)
    print(xvals.shape)

    mag_field = np.sqrt(data['noise'][...,0]**2+data['noise'][...,1]**2)
    print(mag_field.shape)
    

    #Plot scalar magnitude field
    if tau==float('inf'):
        im = ax.imshow(mag_field[-1,...].T, origin='lower', interpolation='bilinear', extent=(-Lx/2.0,Lx/2.0,-Ly/2.0,Ly/2.0), vmin=0.0, cmap='Reds')
    else:
        im = ax.imshow(mag_field[indices[i]+1,...].T, origin='lower', interpolation='bilinear', extent=(-Lx/2.0,Lx/2.0,-Ly/2.0,Ly/2.0), vmin=0.0, cmap='Reds')

    #Plot vector field
    if tau==float('inf'):
        ax.quiver(xvals, yvals, data['noise'][-1,...,0].T, data['noise'][-1,...,1].T, scale_units='xy', scale=4.0, width=0.003, color='black')
    else:
        ax.quiver(xvals, yvals, data['noise'][indices[i]+1,...,0].T, data['noise'][indices[i]+1,...,1].T, scale_units='xy', scale=4.0, width=0.003, color='black')
    ax.set_aspect('equal')
        
    #Particles
    if i==0:
        myfile = 'data/noise_particle_corr/traj_wca_phi=0.1_%s_lambda=%.0f.gsd' % (taustr, Lambda)
    if i==1:
        myfile = 'data/noise_particle_corr/traj_wca_phi=0.4_%s_lambda=%.0f.gsd' % (taustr, Lambda)
        print(myfile)
    if i==2:
        myfile = 'data/noise_particle_corr/traj_none_%s_lambda=%.0f.gsd' % (taustr, Lambda)

    traj = io.load_traj(myfile)
    if traj['edges'].shape[0]<3:
        traj['edges'] = np.append(traj['edges'], 0.0)

    Lx = traj['edges'][0]
    Ly = traj['edges'][1]
    
    active_forces = traj['active_force']
    if i==1:
        print(traj['times'])

    #print(active_forces.shape)

    #ax.scatter(traj['pos'][-1,:,0], traj['pos'][-1,:,1], s=pointsize, linewidths=0.0, c='blue', alpha=0.5)
    ax.quiver(traj['pos'][indices[i],:,0], traj['pos'][indices[i],:,1], active_forces[indices[i],:,0], active_forces[indices[i],:,1], scale_units='xy', scale=2.0, width=0.004, color='blue')
    if i==2:
        ax.set_xlim([Lx/4+(Lx/12),Lx/2])
        ax.set_ylim([-Ly/8+(Ly/12),Ly/8])
    else:
        ax.set_xlim([0,Lx/4-0.5])
        ax.set_ylim([-Ly/2+0.5,-Ly/4])
        #ax.set_xlim([-Lx/2,-Lx/4])
        #ax.set_ylim([-Ly/2+0.5,-Ly/4])
        #ax.set_xlim([Lx/9,Lx/4-0.5-Lx/20])
        #ax.set_ylim([-Ly/2+0.5+Lx/9,-Ly/4-Ly/20])
        #ax.set_xlim([-Lx/2,Lx/2])
        #ax.set_ylim([-Ly/2,Ly/2])
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)
    
    myxmin = -Lx/2+10
    ax.hlines(y=-Ly/2+10, xmin=myxmin, xmax=myxmin+lambdas[j], color='black', linewidth=0.8)
    
plt.savefig('figures/v2/fig_particle_noise_corr.png', dpi=2400)