import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.structure_factor as sq
import AnalysisTools.trajectory_stats as stats

kT=0.0
phi=0.1
va=1.0
taus = [0.1, 1.0, 10.0, float('inf')]
lambdas = [1.0, 3.0, 10.0, 30.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'

num_bins = int(2.0/(2*np.pi/Lx))#1000
print('num bins:', num_bins)

Lambda = lambdas[-1]
tau = taus[-1]

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)

if tau==float('inf'):
    basedir += '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
else:
    basedir += '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)

#if os.path.isfile(myfile):
fig = plt.figure()
data = sq.rebin_sq(basedir)
sq_data = stats.get_postprocessed_stats(data)
#sq_data= np.load(myfile)
sq = sq_data['sq_vals_1d_4_avg']#(sq_data['sq_vals_4_avg'] + sq_data['sq_vals_3_avg'] + sq_data['sq_vals_2_avg']+ sq_data['sq_vals_1_avg'])/4.0
sqerr = sq_data['sq_vals_1d_4_stderr']
q = sq_data['qvals_1d_avg']
print(np.max(q))
print(q)
print(sq)
plt.plot(q,sq)
plt.fill_between(q,sq-2*sqerr, sq+2*sqerr,alpha=0.5)
plt.xlabel(r'$q$')
plt.ylabel(r'$S(q)$')
#plt.legend(fontsize=10)
ax = plt.gca()
#ax.set_aspect('equal')
plt.xlim([-0.02,1.0])
#plt.ylim([-0.02,1.0])
plt.savefig('plots/2d/phi=%f/sq_1d_va=%f_Lambda=%f_tau=%f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lambda, tau, Lx, Ly), dpi=300, bbox_inches='tight')
