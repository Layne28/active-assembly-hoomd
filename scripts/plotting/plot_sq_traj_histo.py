import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

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

Lambda = lambdas[2]
tau = taus[2]

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)

if tau==float('inf'):
    basedir += '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
else:
    basedir += '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)

#if os.path.isfile(myfile):
fig = plt.figure()
data = dict(np.load(basedir+'seed=1/prod/sq_traj.npz'))
print(data.keys())
#sq = sq_data['sq_vals_1d_4_avg']
#sqerr = sq_data['sq_vals_1d_4_stderr']
qstar = data['qvals_1d'][1]
times = data['times']
sq=data['sq_vals']
print(sq)
print('q*', qstar)
colors=plt.get_cmap('viridis')
maxnummode=10
print(data['qvals'].shape)
qs = data['qvals'][:(maxnummode+1),:]
print(qs)
for i in range(1,maxnummode+1):
    plt.plot(times,sq[:,i],c=colors(np.linalg.norm(qs[i,:])/(np.linalg.norm(qs[-1,:]))))
#plt.fill_between(q,sq-2*sqerr, sq+2*sqerr,alpha=0.5)
plt.xlabel(r'$t$')
plt.ylabel(r'$S(q*)(t)$')
#plt.legend(fontsize=10)
#ax.set_aspect('equal')
#plt.xlim([-0.02,1.0])
#plt.ylim([-0.02,1.0])
plt.savefig('plots/2d/phi=%f/sq_traj_top%d_va=%f_Lambda=%f_tau=%f_Lx=%.01f_Ly=%.01f.png' % (phi, maxnummode, va, Lambda, tau, Lx, Ly), dpi=300, bbox_inches='tight')
