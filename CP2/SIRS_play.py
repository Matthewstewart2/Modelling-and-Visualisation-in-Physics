"""
2D SIRS model animation
periodic boundary conditions

Must specify system size, p1, p2 and p3
"""

from SIRS_class import SIRS_lattice2D
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    # Remind user of correct command line arguments if needed
    if(len(sys.argv) != 5):
        print ("Usage python SIRS_play.py N p1 p2 p3")
        sys.exit()
    N = int(sys.argv[1])
    p1 = float(sys.argv[2])
    p2 = float(sys.argv[3])
    p3 = float(sys.argv[4])
    Simulation = SIRS_lattice2D(N, p1, p2, p3)
    Simulation.play_simulation()
    
main()