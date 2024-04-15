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

Lambda = lambdas[3]
tau = taus[-1]

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)

if tau==float('inf'):
    basedir += '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
else:
    basedir += '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)

#if os.path.isfile(myfile):
fig = plt.figure()
for i in range(1,11):
    data = dict(np.load(basedir+'seed=%d/prod/energies_and_forces.npz' % i))
    #plt.plot(data['times'], data['potential_energy'], label='potential')
    plt.plot(data['times'], data['kinetic_energy'], linewidth=0.5)#, label='kinetic')
    if data['times'][-1]>1000:
        print(i)
#plt.legend()
plt.ylim([0,2000])
plt.xlim([0,1000])
plt.xlabel(r'$t$')
plt.ylabel(r'$E$')
if not os.path.exists('plots/2d/phi=%f/energies_and_forces/' % phi):
    os.makedirs('plots/2d/phi=%f/energies_and_forces/' % phi)
plt.savefig('plots/2d/phi=%f/energies_and_forces/energy_va=%f_Lambda=%f_tau=%f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lambda, tau, Lx, Ly), dpi=300, bbox_inches='tight')
