from Ising2D_1 import Lattice2D
import sys
import numpy as np
import matplotlib.pyplot as plt
import random

def main1():
    #
    if(len(sys.argv) != 3):
        print ("Usage python Ising2D_play.animation.py N T")
        sys.exit()
    
    lx=int(sys.argv[1]) 
    ly=lx 
    kT=float(sys.argv[2])
    dynamics = input('\'1\' for Glauber dynamics, \'2\' for Kawasaki dynamics: ')
    spins=np.zeros((lx,ly),dtype=int)
    # random initial configuration
    for i in range(lx):
        for j in range(ly):
            r=random.random()
            if(r<0.5): spins[i,j]=-1
            if(r>=0.5): spins[i,j]=1
    Simulation = Lattice2D(lx, ly, kT, dynamics, spins)
    Simulation.play_simulation()
    
def main2():
    #
    if(len(sys.argv) != 4):
        print ("Usage python Ising2D_play.animation.py N T1 T2")
        sys.exit()
    
    lx=int(sys.argv[1]) 
    ly=lx 
    delta_t = 0.1
    kTs=np.arange(float(sys.argv[2]), float(sys.argv[3])+delta_t, delta_t)
    dynamics = input('\'1\' for Glauber dynamics, \'2\' for Kawasaki dynamics: ')
    if dynamics == '1':
        avg_absMs = np.zeros(len(kTs))
        avg_Es = np.zeros(len(kTs))
        suscepts = np.zeros(len(kTs))
        heat_caps = np.zeros(len(kTs))
        start_spins = np.ones((lx,ly),dtype=int)
        for i in range(len(kTs)):        
            Simulation = Lattice2D(lx, ly, kTs[i], dynamics, start_spins)
            avg_absM, avg_E, suscept, heat_cap, start_spins = Simulation.play_simulation(animate=False)
            avg_absMs[i] = avg_absM
            avg_Es[i] = avg_E
            suscepts[i] = suscept
            heat_caps[i] = heat_cap
            print('done kT = ', kTs[i])
        fig, axs = plt.subplots(2, 2, sharex=True, figsize=(12,10))
        fig.suptitle('Glauber')
        fig.supxlabel('kT')
        axs[0, 0].plot(kTs, avg_absMs, color='k')
        axs[0, 0].set_ylabel(r'$\left \langle \left | M \right | \right \rangle$', rotation=0)
        axs[0, 1].plot(kTs, suscepts, color='g')
        axs[0, 1].set_ylabel(r'$\chi$', rotation=0)
        axs[1, 0].plot(kTs, avg_Es, color='r')
        axs[1, 0].set_ylabel(r'$\left \langle E \right \rangle$', rotation=0)
        axs[1, 1].plot(kTs, heat_caps, color='b')
        axs[1, 1].set_ylabel(r'$C$', rotation=0)
        plt.show()
    else:
        avg_Es = np.zeros(len(kTs))
        heat_caps = np.zeros(len(kTs))
        num_downs = (lx*ly) // 2
        num_ups = lx*ly - num_downs
        start_spins = np.concatenate([np.ones(num_ups, dtype=int), -np.ones(num_downs, dtype=int)], dtype=int)
        start_spins = np.reshape(start_spins, (lx, ly))
        for i in range(len(kTs)):        
            Simulation = Lattice2D(lx, ly, kTs[i], dynamics, start_spins)
            avg_E, heat_cap, start_spins = Simulation.play_simulation(animate=False)
            avg_Es[i] = avg_E
            heat_caps[i] = heat_cap
            print('done kT = ', kTs[i])
        fig, axs = plt.subplots(1, 2, sharex=True, figsize=(12,10))
        fig.suptitle('Kawasaki')
        fig.supxlabel('kT')
        axs[0].plot(kTs, avg_Es, color='r')
        axs[0].set_ylabel(r'$\left \langle E \right \rangle$', rotation=0)
        axs[1].plot(kTs, heat_caps, color='b')
        axs[1].set_ylabel(r'$C$', rotation=0)
        plt.show()
        

#main1()
main2()