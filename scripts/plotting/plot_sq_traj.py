import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

kT=0.0
phi=0.1
va=1.0
taus = [0.1, 1.0, 10.0, 100.0, float('inf')]
lambdas = [1.0, 3.0, 5.0, 10.0]
Lx=200.000000
Ly=200.000000
nx=400
ny=400
interpolation='linear'
compressibility='compressible'
cov_type='exponential'

Lambda = lambdas[1]
tau = taus[-2]

print('lambda', Lambda)
print('tau', tau)

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/manyseed/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)

if tau==float('inf'):
    basedir += '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
else:
    basedir += '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)

#if os.path.isfile(myfile):
fig = plt.figure()
data = dict(np.load(basedir+'seed=3/prod/sq_traj.npz'))
print(data.keys())
#sq = sq_data['sq_vals_1d_4_avg']
#sqerr = sq_data['sq_vals_1d_4_stderr']
times = data['times']
sq=data['sq_vals']
qmag = data['qmag']

#sort by qmag
inds = qmag.argsort()
print(qmag[inds])
qmag = qmag[inds]
sq = sq[:,inds]
qs = data['qvals'][inds,:]

maxnummode=10
qs = qs[:(maxnummode+1),:]
print(qs)
colors=plt.get_cmap('viridis')
for i in range(0,maxnummode):
    print(qs[i,:])
    print((np.linalg.norm(qs[i,:])-np.linalg.norm(qs[0,:]))/((np.linalg.norm(qs[-1,:])-np.linalg.norm(qs[0,:]))))
    #print(np.linalg.norm(qs[i,:]))#/(np.linalg.norm(qs[-1,:])))
    #plt.plot(times,sq[:,i],c=colors(np.linalg.norm(qs[i,:])/(np.linalg.norm(qs[-1,:]))),zorder=i)
    plt.plot(times,sq[:,i],c=colors((np.linalg.norm(qs[i,:])-np.linalg.norm(qs[0,:]))/((np.linalg.norm(qs[-1,:])-np.linalg.norm(qs[0,:])))),zorder=maxnummode-i)
    #plt.plot(times,sq[:,i],c=colors(i/maxnummode),zorder=maxnummode-i)
#plt.fill_between(q,sq-2*sqerr, sq+2*sqerr,alpha=0.5)
plt.xlabel(r'$t$')
plt.ylabel(r'$S(q*)(t)$')
#plt.legend(fontsize=10)
#ax.set_aspect('equal')
#plt.xlim([-0.02,1.0])
#plt.ylim([-0.02,1.0])
plt.savefig('plots/2d/phi=%f/sq_traj_top%d_va=%f_Lambda=%f_tau=%f_Lx=%.01f_Ly=%.01f.png' % (phi, maxnummode, va, Lambda, tau, Lx, Ly), dpi=300, bbox_inches='tight')
