"""
2D Ising model simulation to estimate critical temperature

Can specify:
    lattice size but is always square
    temperature range
    dynamics (Glauber or Kawasaki)
    
Saves graphs and writes data to file
"""

from Ising2D_class import Lattice2D
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
    
def main():
    # if user doesn't remember or incorrectly puts arguments on command line, remind them of format
    if(len(sys.argv) != 4):
        print ("Usage python Ising2D_play.animation.py N T1 T2")
        sys.exit()
    
    lx=int(sys.argv[1]) 
    ly=lx
    # always separates kTs by 0.1 but could change
    delta_t = 0.1
    # includes T2
    kTs=np.arange(float(sys.argv[2]), float(sys.argv[3])+delta_t, delta_t)
    dynamics = input('\'1\' for Glauber dynamics, \'2\' for Kawasaki dynamics: ')
    # make arrays to store data for plotting
    if dynamics == '1':
        # for Glauber dynamics
        avg_absMs = np.zeros(len(kTs))
        avg_absMs_err = np.zeros(len(kTs))
        avg_Es = np.zeros(len(kTs))
        avg_Es_err = np.zeros(len(kTs))
        suscepts = np.zeros(len(kTs))
        suscepts_err = np.zeros(len(kTs))
        heat_caps = np.zeros(len(kTs))
        heat_caps_err = np.zeros(len(kTs))
        # initial configuration is what we expect for low T ie all ordered
        start_spins = np.ones((lx,ly),dtype=int)
        # run simulation for each kT and record data with errors
        for i in range(len(kTs)):        
            Simulation = Lattice2D(lx, ly, kTs[i], dynamics, start_spins)
            avg_absM, avg_E, suscept, heat_cap, start_spins = Simulation.play_simulation(animate=False)
            avg_absMs[i] = avg_absM[0]
            avg_absMs_err[i] = avg_absM[1]
            avg_Es[i] = avg_E[0]
            avg_Es_err[i] = avg_E[1]
            suscepts[i] = suscept[0]
            suscepts_err[i] = suscept[1]
            heat_caps[i] = heat_cap[0]
            heat_caps_err[i] = heat_cap[1]
            # message to show how many temperatures are remaining
            print('done kT = ', kTs[i])
        # write to csv file
        csvtitle = ['# 2D Ising Model Glauber Dynamics Data']
        csvheader = ['kTs', 'avg_absMs', 'avg_absMs_err', 'suscepts', 'suscepts_err',
                     'avg_Es', 'avg_Es_err', 'heat_caps', 'heat_caps_err']
        csvdata = np.array([kTs, avg_absMs, avg_absMs_err, suscepts, suscepts_err,
                            avg_Es, avg_Es_err, heat_caps, heat_caps_err]).T
        with open('Ising2D_Glauber_data.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csvtitle)
            writer.writerow(csvheader)
            writer.writerows(csvdata)
        # make plots with errors
        fig, axs = plt.subplots(2, 2, figsize=(12,10))
        fig.suptitle('Glauber Dynamics')
        fig.supxlabel('kT')
        axs[0, 0].errorbar(kTs, avg_absMs, yerr=avg_absMs_err, fmt='k.', ecolor='k', capsize=3)
        axs[0, 0].set_ylabel(r'$\left \langle \left | M \right | \right \rangle$', rotation=0, labelpad=22)
        axs[0, 1].errorbar(kTs, suscepts, yerr=suscepts_err, fmt='g.', ecolor='k', capsize=3)
        axs[0, 1].set_ylabel(r'$\chi$', rotation=0, labelpad=22)
        axs[1, 0].errorbar(kTs, avg_Es, yerr=avg_Es_err, fmt='r.', ecolor='k', capsize=3)
        axs[1, 0].set_ylabel(r'$\left \langle E \right \rangle$', rotation=0, labelpad=22)
        axs[1, 1].errorbar(kTs, heat_caps, yerr=heat_caps_err, fmt='b.', ecolor='k', capsize=3)
        axs[1, 1].set_ylabel(r'$C$', rotation=0, labelpad=22)
        # all plots saved to one file
        plt.savefig('Glauber_plots')
        plt.show()
    else:
        # for Kawasaki dynamics
        avg_Es = np.zeros(len(kTs))
        avg_Es_err = np.zeros(len(kTs))
        heat_caps = np.zeros(len(kTs))
        heat_caps_err = np.zeros(len(kTs))
        # initial state is now domains of all up and all down with minimum interface  between them
        # // is floor division so if odd number of spins extra one will be +1 spin initially
        num_downs = (lx*ly) // 2
        num_ups = lx*ly - num_downs
        start_spins = np.concatenate([np.ones(num_ups, dtype=int), -np.ones(num_downs, dtype=int)], dtype=int)
        start_spins = np.reshape(start_spins, (lx, ly))
        for i in range(len(kTs)):        
            Simulation = Lattice2D(lx, ly, kTs[i], dynamics, start_spins)
            avg_E, heat_cap, start_spins = Simulation.play_simulation(animate=False)
            avg_Es[i] = avg_E[0]
            avg_Es_err[i] = avg_E[1]
            heat_caps[i] = heat_cap[0]
            heat_caps_err[i] = heat_cap[1]
            print('done kT = ', kTs[i])
        # write csv file
        csvtitle = ['# 2D Ising Model Kawasaki Dynamics Data']
        csvheader = ['kTs', 'avg_Es', 'avg_Es_err', 'heat_caps', 'heat_caps_err']
        csvdata = np.array([kTs, avg_Es, avg_Es_err, heat_caps, heat_caps_err]).T
        with open('Ising2D_Kawasaki_data.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csvtitle)
            writer.writerow(csvheader)
            writer.writerows(csvdata)
        
        fig, axs = plt.subplots(1, 2, sharex=True, figsize=(12,10))
        fig.suptitle('Kawasaki Dynamics')
        fig.supxlabel('kT')
        axs[0].errorbar(kTs, avg_Es, yerr=avg_Es_err, fmt='r.', ecolor='k', capsize=3)
        axs[0].set_ylabel(r'$\left \langle E \right \rangle$', rotation=0, labelpad=22)
        axs[1].errorbar(kTs, heat_caps, yerr=heat_caps_err, fmt='b.', ecolor='k', capsize=3)
        axs[1].set_ylabel(r'$C$', rotation=0, labelpad=22)
        plt.savefig('Kawasaki_plots')
        plt.show()
        
main()