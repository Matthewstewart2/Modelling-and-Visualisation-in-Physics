"""
2D SIRS model phase diagram experiment
periodic boundary conditions

Must specify system size
"""

from SIRS_class import SIRS_lattice2D
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    # Remind user of correct command line arguments if needed
    if(len(sys.argv) != 2):
        print ("Usage python SIRS_phases.py N")
        sys.exit()
    N = int(sys.argv[1])
    # Scan p1 and p3 from 0 to 1 while fixing p2=0.5
    start = 0
    stop = 1.
    step = 0.05
    p1s = np.arange(start, stop+step, step)
    p2 = 0.5
    p3s = np.arange(start, stop+step, step)
    # Make a grid for mean infected fractions for imshow
    mean_infected_grid = np.zeros((len(p3s), len(p1s)))
    # Another for variance
    variance_grid = np.zeros((len(p3s), len(p1s)))
    # These will be the same data but in columns instead of grid to write to file
    file_p1s = []
    file_p3s = []
    file_mean_infected = []
    file_variance = []
    for i in range(len(p1s)):
        for j in range(len(p3s)): 
            file_p1s.append(p1s[i])
            file_p3s.append(p3s[j])
            Simulation = SIRS_lattice2D(N, p1s[i], p2, p3s[j])
            # Calculate mean infected fraction and variance
            mean_infected, variance = Simulation.play_simulation(animate=False, get_error=False)
            mean_infected_grid[i, j] = mean_infected
            file_mean_infected.append(mean_infected)
            variance_grid[i, j] = variance[0]
            file_variance.append(variance[0])
            
    csvtitle = ['# SIRS model phase diagram data p2 = 0.5']
    csvheader = ['p1', 'p3', 'mean_I', 'variance_I']
    # Transpose to sort data into columns
    csvdata = np.array([file_p1s, file_p3s, file_mean_infected, file_variance]).T
    with open('SIRS_phase_diagram.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvtitle)
        writer.writerow(csvheader)
        writer.writerows(csvdata)
        
    # Make plots
    fig, axs = plt.subplots(1, 2, figsize=(12,6))
    # Left is mean infected fraction grid, ie. phase diagram
    axs[0].set_title('Mean infected fraction')
    im1 = axs[0].imshow(mean_infected_grid, cmap='coolwarm', origin='lower')
    plt.colorbar(im1, ax=axs[0])
    axs[0].set_xlabel('p1')
    axs[0].set_ylabel('p3')
    axs[0].set_xticks(np.arange(0, len(p1s), 4))
    axs[0].set_xticklabels(np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
    axs[0].set_yticks(np.arange(0, len(p1s), 4))
    axs[0].set_yticklabels(np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
    # Right is variance plot where maximum variance should show where waves appear
    axs[1].set_title('Scaled variance of number of infected sites' )
    im2 = axs[1].imshow(variance_grid, cmap='BrBG', origin='lower')
    plt.colorbar(im2, ax=axs[1])
    axs[1].set_xlabel('p1')
    axs[1].set_ylabel('p3')
    axs[1].set_xticks(np.arange(0, len(p1s), 4))
    axs[1].set_xticklabels(np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
    axs[1].set_yticks(np.arange(0, len(p1s), 4))
    axs[1].set_yticklabels(np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
    plt.show()
    
   
    
main()