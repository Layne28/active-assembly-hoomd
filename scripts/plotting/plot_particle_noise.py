import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec

import AnalysisTools.particle_io as io


fig, ax = plt.subplots(1,1)

index = 3

srate = 1
maxlim=50
buffer=0.1
data = io.load_noise_traj('/pscratch/sd/l/lfrechet/active-assembly-hoomd/test/noise/2d/tau=0.100000/lambda=20.000000/nx=400_ny=400/compressible/exponential/seed=1/noise_traj.h5')

Lx = data['ncells'][0]*data['spacing'][0]
Ly = data['ncells'][1]*data['spacing'][1]
#xvals = np.arange(data['ncells'][0])*data['spacing'][0]-Lx/2.0
#yvals = np.arange(data['ncells'][1])*data['spacing'][1]-Ly/2.0
xvals, yvals = np.meshgrid(np.linspace(0,data['ncells'][0]*data['spacing'][0],data['ncells'][0])-Lx/2.0,
np.linspace(0,data['ncells'][1]*data['spacing'][1],data['ncells'][1])-Ly/2.0)
print(xvals.shape)

mag_field = np.sqrt(data['noise'][...,0]**2+data['noise'][...,1]**2)


#Plot scalar magnitude field
im = ax.imshow(mag_field[index+1,...].T, origin='lower', interpolation='bilinear', extent=(-Lx/2.0,Lx/2.0,-Ly/2.0,Ly/2.0), vmin=0.0, cmap='Reds')
#ax[i].set_xlim([-buffer,maxlim+buffer])
#ax[i].set_ylim([-buffer,maxlim+buffer])
#ax[i].set_title(r'$\lambda_{\text{a}}=%.0f$' % lambdas[i], fontsize=10, pad=8.0)

#Plot vector field
ax.quiver(xvals[::srate,::srate], yvals[::srate,::srate], data['noise'][index+1,::srate,::srate,0].T, data['noise'][index+1,::srate,::srate,1].T, scale_units='xy', scale=2.0, width=0.003, color='black')
#ax.quiver(xvals, yvals, data['noise'][-1,...,0].T, data['noise'][-1,...,1].T, scale_units='xy', scale=4.0, width=0.003, color='white')
ax.set_aspect('equal')
#ax[i].set_xlabel(r'$x/\sigma$',labelpad=1,fontsize=10)
#if i==0:
#    ax[i].set_ylabel(r'$y/\sigma$', fontsize=10)
    
    
#Particles
myfile = '/pscratch/sd/l/lfrechet/active-assembly-hoomd/test/wca/2d/kT=0.000000/phi=0.400000/va=1.000000/tau=0.100000/lambda=20.000000/Lx=200.000000_Ly=200.000000/nx=400_ny=400/interpolation=linear/compressible/exponential/seed=1/prod/traj.gsd'

traj = io.load_traj(myfile)
if traj['edges'].shape[0]<3:
    traj['edges'] = np.append(traj['edges'], 0.0)

Lx = traj['edges'][0]
Ly = traj['edges'][1]

active_forces = traj['active_force']

#ax.scatter(traj['pos'][-1,:,0], traj['pos'][-1,:,1], s=pointsize, linewidths=0.0, c='blue', alpha=0.5)
ax.quiver(traj['pos'][index,:,0], traj['pos'][index,:,1], active_forces[index,:,0], active_forces[index,:,1], scale_units='xy', scale=2.0, width=0.003, color='blue')
ax.set_xlim([Lx/4+(Lx/12),Lx/2])
ax.set_ylim([-Ly/8+(Ly/12),Ly/8])
#ax.set_xlim([Lx/9,Lx/4-0.5-Lx/20])
#ax.set_ylim([-Ly/2+0.5+Lx/9,-Ly/4-Ly/20])
#ax.set_xlim([-Lx/2,Lx/2])
#ax.set_ylim([-Ly/2,Ly/2])
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.xaxis.set_tick_params(labelbottom=False)
ax.yaxis.set_tick_params(labelleft=False)
    
plt.savefig('fig_particle_noise_corr.png', dpi=600)