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

num_bins = 100

Lambda = lambdas[1]
tau = taus[1]

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)

fig = plt.figure()
if tau==float('inf'):
    myfile = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/sq_avg.npz' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
else:
    myfile = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/sq_avg.npz' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)

if os.path.isfile(myfile):
    sq_data= np.load(myfile)
    sq = sq_data['sq_vals_4_avg']#(sq_data['sq_vals_4_avg'] + sq_data['sq_vals_3_avg'] + sq_data['sq_vals_2_avg']+ sq_data['sq_vals_1_avg'])/4.0
    q = sq_data['qvals_avg']
    im = plt.scatter(q[1:,0],q[1:,1],c=sq[1:],s=10)
    plt.xlabel(r'$qx$')
    plt.ylabel(r'$qy$')
    #plt.legend(fontsize=10)
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.xlim([-0.02,1.0])
    plt.ylim([-0.02,1.0])
    plt.savefig('plots/2d/phi=%f/sq_2d_va=%f_Lambda=%f_tau=%f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lambda, tau, Lx, Ly), dpi=300, bbox_inches='tight')
