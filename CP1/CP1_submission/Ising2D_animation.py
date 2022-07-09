"""
2D Ising model animation using plt.imshow

Can specify:
    lattice size but is always square
    temperature
    dynamics (Glauber or Kawasaki)
"""

from Ising2D_class import Lattice2D
import sys
import numpy as np
import random

def main():
    # if user doesn't remember or incorrectly puts arguments on command line, remind them of format
    if(len(sys.argv) != 3):
        print ("Usage python Ising2D_play.animation.py N T")
        sys.exit()
    
    lx=int(sys.argv[1]) 
    ly=lx 
    kT=float(sys.argv[2])
    # prompt user for choice of dynamics
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
    
main()