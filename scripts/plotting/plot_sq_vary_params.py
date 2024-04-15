import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import AnalysisTools.structure_factor as sq
import AnalysisTools.trajectory_stats as stats

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

#num_bins = 1000
num_bins = int(2.0/(2*np.pi/Lx))#1000
print('num bins:', num_bins)

#colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))
colors_tau = mpl.cm.plasma(np.linspace(0,1,len(taus)))

basedir = os.environ['SCRATCH'] + '/active-assembly-hoomd/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va)


for Lambda in lambdas:
    fig = plt.figure()
    for i in range(len(taus)):
        tau = taus[i]
        if tau==float('inf'):
            thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        else:
            thedir = basedir + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (tau, Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        print('tau:', tau)
        data = sq.rebin_sq(thedir)
        sq_data = stats.get_postprocessed_stats(data)
        sqavg = (sq_data['sq_vals_1d_4_avg']+sq_data['sq_vals_1d_3_avg']+sq_data['sq_vals_1d_2_avg']+sq_data['sq_vals_1d_1_avg'])/4.0
        sqerr = sq_data['sq_vals_1d_4_stderr']
        q1d = sq_data['qvals_1d_avg']
        themax = np.max(sqavg)
        theargmax = np.argmax(sqavg)
        plt.plot(q1d,sqavg,color=colors_tau[i], label=r'$\tau_a=%.01f$' % taus[i])
        plt.fill_between(q1d, sqavg-2*sqerr, sqavg+2*sqerr, color=colors_tau[i], alpha=0.4)
        plt.scatter(q1d[theargmax], themax, c='black', marker='*', s=35.0,zorder=10)
        plt.scatter(q1d[theargmax], themax, c=colors_tau[i], marker='*', s=15.0, zorder=11)
        #plt.scatter(q1d[1:-1],sqavg[1:],c=colors_tau[i], label=r'$\tau_a=%.01f$' % taus[i])
        #plt.plot(q[1:-1],sq[1:],color=colors_tau[i], label=r'$\tau_a=%.01f$' % taus[i])
    #plt.xlim([-0.1,15.1])
    #plt.ylim([0,8])
    plt.xlabel(r'$q$')
    plt.ylabel(r'$S(q)$')
    plt.legend(fontsize=10)
    plt.xlim([0.0,1.0])
    plt.savefig('plots/2d/phi=%f/sq_1d_vary_tau_va=%f_Lambda=%f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lambda, Lx, Ly), dpi=300, bbox_inches='tight')

#Quenched case
fig, axs = plt.subplots(1,1)
#phis = [0.1,0.4]
phis=[phi]
cnt=0
for phi in phis:
    for i in range(len(lambdas)):
        Lambda = lambdas[i]
        thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
        data = sq.rebin_sq(thedir)
        sq_data = stats.get_postprocessed_stats(data)
        sqavg = sq_data['sq_vals_1d_4_avg']
        sqerr = sq_data['sq_vals_1d_4_stderr']
        q1d = sq_data['qvals_1d_avg']
        axs.plot(q1d,sqavg, label=r'$\lambda_a=%.01f$' % Lambda)
        axs.fill_between(q1d, sqavg+2*sqerr, sqavg-2*sqerr, alpha=0.4)
        #axs.scatter(q1d[1:-1],sqavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)
        #axs.plot(q1d[1:-1],sqavg[1:], label=r'$\lambda_a=%.01f$' % Lambda)

        axs.set_xlabel(r'$q\sigma$')
        axs.set_ylabel(r'$S(q)$')

        axs.legend()

        cnt+=1
        
        axs.set_xlim([-0.01,1.0])
        #axs.set_ylim([-0.01,200])
plt.yscale('log')
plt.tight_layout()
plt.savefig('plots/2d/sq_quenched_vary_lambda_phi=%.01f_va=%.01f_Lx=%.01f_Ly=%.01f.png' % (phi, va, Lx, Ly), dpi=300, bbox_inches='tight')

'''
fig, axs = plt.subplots(2,1, figsize=(3.75,3.3),sharex=True, sharey=True)
#phis = [0.1,0.4]
phis=[0.1]
cnt=0
for phi in phis:
    file1 = os.environ['WORK'] + '/active-assembly/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va) + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/sq_avg.npz' % (taus[-1], 3.0, Lx, Ly, nx, ny, interpolation, compressibility)
    file2 = os.environ['WORK'] + '/active-assembly/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va) + '/tau=%f/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/sq_avg.npz' % (taus[-1], 10.0, Lx, Ly, nx, ny, interpolation, compressibility)

    sq_data= np.load(file1)
    sq = sq_data['sq_vals_1d_4_avg']
    q = sq_data['qvals_1d_avg']
    axs[cnt].plot(q[1:-1],sq[1:],color='red', label=r'$\lambda_a=3.0$')

    sq_data= np.load(file2)
    sq = sq_data['sq_vals_1d_4_avg']
    q = sq_data['qvals_1d_avg']
    axs[cnt].plot(q[1:-1],sq[1:],color='blue', label=r'$\lambda_a=10.0$')

    #axs[cnt].set_title(r'$\phi=%.01f$' % phi)
    axs[cnt].text(3.0, 6.0, r'$\phi=%.01f$' % phi, ha='center')
    axs[1].set_xlabel(r'$q\sigma$')
    axs[cnt].set_ylabel(r'$S(q)$')

    axs[0].legend()

    cnt+=1
plt.tight_layout()
plt.savefig('plots/2d/sq_quenched_vary_phi_lambda_va=%f_Lx=%.01f_Ly=%.01f.png' % (va, Lx, Ly), dpi=300, bbox_inches='tight')

fig = plt.figure()
vas = [0.1,0.3,1.0,3.0]
colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))

Lambda=3.0
phi=0.1

for i in range(len(vas)):
    va = vas[i]

    file = os.environ['SCRATCH'] + '/active-assembly-hoomd/wca/2d/kT=%f/phi=%f/va=%f' % (kT, phi, va) + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/sq_avg.npz' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
    if os.path.isfile(file):
        sq_data= np.load(file)
        sq = (sq_data['sq_vals_1d_4_avg'] + sq_data['sq_vals_1d_3_avg'] + sq_data['sq_vals_1d_2_avg'])/3.0
        q = sq_data['qvals_1d_avg']
        plt.plot(q[1:-1],sq[1:],color=colors_va[i], label=r'$v_a=%.01f$' % va)

plt.legend()
plt.xlabel(r'$q\sigma$')
plt.ylabel(r'$S(q)$')
plt.savefig('plots/2d/sq_quenched_vary_va_lambda=%.01f_phi=%.01f_Lx=%.01f_Ly=%.01f.png' % (Lambda, phi, Lx, Ly), dpi=300, bbox_inches='tight')
'''


fig = plt.figure()
vas = [0.1,0.3,1.0,3.0]
colors_va = mpl.cm.plasma(np.linspace(0,1,len(vas)))

Lambda=3.0

va = 1.0

thedir = basedir + '/quenched/lambda=%f/Lx=%f_Ly=%f/nx=%d_ny=%d/interpolation=%s/%s/%s/' % (Lambda, Lx, Ly, nx, ny, interpolation, compressibility, cov_type)
data2 = sq.rebin_sq(thedir)
for d in data2:
    print('test2qmax:', np.max(d['qvals_1d']))
sq_post = stats.get_postprocessed_stats(data2)
sqavg = sq_post['sq_vals_1d_4_avg']
sqerr = sq_post['sq_vals_1d_4_stderr']
for d in data2:
    #sq_data= (d['sq_vals_1d_4'] + d['sq_vals_1d_3'] + d['sq_vals_1d_2']+ d['sq_vals_1d_1'])/4.0
    sq_data= d['sq_vals_1d_4']
    #sq = (sq_data['sq_vals_1d_4_avg'] + sq_data['sq_vals_1d_3_avg'] + sq_data['sq_vals_1d_2_avg'])/3.0
    q = d['qvals_1d']
    print(np.max(q))
    plt.plot(q,sq_data, linewidth=0.5)
plt.plot(q, sqavg, color='black')

#plt.legend()
plt.xlabel(r'$q\sigma$')
plt.ylabel(r'$S(q)$')
plt.savefig('plots/2d/sq_quenched_multitraj_lambda=%.01f_phi=%.01f_Lx=%.01f_Ly=%.01f.png' % (Lambda, phi, Lx, Ly), dpi=300, bbox_inches='tight')