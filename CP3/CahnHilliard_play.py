"""
Animate phase separation characterised by Cahn-Hilliard eqn.

User can specify system size and various constants
including initial phi0
"""

from CahnHilliard_class import CahnHilliard_lattice2D
import sys
import numpy as np

def main():
    # Remind user of correct command line arguments if needed
    if(len(sys.argv) != 8):
        print ("Usage python CahnHilliard_play.py a M k N phi0 dx dt")
        sys.exit()
    # Input the various constants of choice
    a = float(sys.argv[1])
    M = float(sys.argv[2])
    k = float(sys.argv[3])
    N = int(sys.argv[4])
    phi0 = float(sys.argv[5])
    dx = float(sys.argv[6])
    dt = float(sys.argv[7])
    Simulation = CahnHilliard_lattice2D(a, M, k, N, phi0, dx, dt)
    Simulation.play_simulation()
    
main()