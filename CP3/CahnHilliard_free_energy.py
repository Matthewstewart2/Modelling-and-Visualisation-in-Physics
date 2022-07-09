"""
Plot free energy against time during phase separation
characterised by Cahn-Hilliard eqn.

User can specify system size and various constants
including initial phi0
"""

from CahnHilliard_class import CahnHilliard_lattice2D
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    # Remind user of correct command line arguments if needed
    if(len(sys.argv) != 8):
        print ("Usage python CahnHilliard_play.py a M k N phi0 dx dt")
        sys.exit()
    a = float(sys.argv[1])
    M = float(sys.argv[2])
    k = float(sys.argv[3])
    N = int(sys.argv[4])
    phi0 = float(sys.argv[5])
    dx = float(sys.argv[6])
    dt = float(sys.argv[7])
    Simulation = CahnHilliard_lattice2D(a, M, k, N, phi0, dx, dt)
    frames, free_energies = Simulation.play_simulation(animate=False)
    
    # Write data to csv file
    csvtitle = ['# Cahn-Hilliard Free Energy']
    csvheader = ['frame, free energy']
    # Transpose to sort data into columns
    csvdata = np.array([frames, free_energies]).T
    with open('CahnHilliard_free_energy_phi{}.csv'.format(phi0), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvtitle)
        writer.writerow(csvheader)
        writer.writerows(csvdata)
        
    # Plot free energy against time
    fig, ax = plt.subplots()
    ax.plot(frames, free_energies, 'r.')
    ax.set_title(r'$\phi_0 = $'+str(phi0))
    ax.set_xlabel('Frame')
    ax.set_ylabel('Free energy')
    plt.show()
    
main()