import numpy as np
import matplotlib.pyplot as plt
import sys

import AnalysisTools.particle_io as io
import AnalysisTools.field_analysis as field_analysis
import AnalysisTools.field_particle_correlation as correlation

traj_name = sys.argv[1]
noise_name = sys.argv[2]

traj = io.load_traj(traj_name)
noise = io.load_noise_traj(noise_name)

nframes = traj['pos'].shape[0]
nskip = int(0.4*nframes)

pressure = -0.5*(traj['virial'][:,:,0] + traj['virial'][:,:,3])
mag_field = np.sqrt(noise['noise'][nskip:,:,:,0]**2+noise['noise'][nskip:,:,:,1]**2)

print(noise['noise'].shape)
div_field = field_analysis.get_divergence(2, noise['ncells'], noise['spacing'], noise['noise'][nskip:,...])

print('div shape')
print(div_field.shape)

pressure_field = correlation.get_pressure_field(nframes, nskip, pressure, traj['pos'], traj['edges'], mag_field, noise['spacing'], noise['ncells'])


fig = plt.figure()
plt.scatter(div_field, pressure_field, s=0.1, alpha=0.5,linewidths=0)
ax = plt.gca()
plt.xlabel('divergence')
plt.ylabel('pressure')
#ax.set_aspect('equal', 'box')
plt.savefig('div_scatter.png')