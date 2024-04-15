import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

kT=0.0
phi=0.4
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

Lambda = lambdas[1]
tau = taus[-1]

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)

if tau==float('inf'):
    basedir += '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
else:
    basedir += '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)

#if os.path.isfile(myfile):
fig = plt.figure()
data = dict(np.load(basedir+'seed=6/prod/energies_and_forces.npz'))
print(data.keys())
for mu in range(2):
    plt.plot(data['times'], data['net_conservative_force'][:,mu], label='conservative', color='blue')
    plt.plot(data['times'], data['net_active_force'][:,mu], label='active', color='red')
plt.legend()
plt.xlabel(r'$t$')
plt.ylabel(r'$E$')
if not os.path.exists('plots/2d/phi=%f/energies_and_forces/' % phi):
    os.makedirs('plots/2d/phi=%f/energies_and_forces/' % phi)
plt.savefig('plots/2d/phi=%f/energies_and_forces/force_va=%f_Lambda=%f_tau=%f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lambda, tau, Lx, Ly), dpi=300, bbox_inches='tight')
