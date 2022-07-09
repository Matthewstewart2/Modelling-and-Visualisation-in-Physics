"""
2D SIRS model immunity fraction experiment
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
    if(len(sys.argv) != 5):
        print ("Usage python SIRS_immunity.py N p1 p2 p3")
        sys.exit()
    N = int(sys.argv[1])
    # Immune fraction from 0 to 1
    start = 0
    stop = 1.0
    num_pts = 51
    p1 = float(sys.argv[2])
    p2 = float(sys.argv[3])
    p3 = float(sys.argv[4])
    immune_frac_array = np.linspace(start, stop, num_pts)
    repeats = 5
    infected_array = np.zeros((repeats, len(immune_frac_array)))
    for i in range(repeats):
        for j in range(len(immune_frac_array)):
            Simulation = SIRS_lattice2D(N, p1, p2, p3, immune_frac_array[j])
            mean_infected, variance = Simulation.play_simulation(animate=False, get_error=False)
            infected_array[i][j] = mean_infected
            # To check how much longer is left
            print('done', immune_frac_array[j], 'repeat', i+1)
    # Wrap in extra array to concatenate together
    infected_means = np.array([np.mean(infected_array, axis=0)])
    infected_sems = np.array([np.std(infected_array, axis=0, ddof=1) / np.sqrt(repeats)])
    data = np.concatenate((np.array([immune_frac_array]), infected_array, infected_means, infected_sems), axis=0)
            
    csvtitle = ['# SIRS model immunity data p1 = {} p2 = {} p3 = {}'.format(p1, p2, p3)]
    csvheader = ['Immune_fraction'] + list(range(1, repeats+1)) + ['mean_I_fraction', 'sem_I_fraction']
    # Transpose to sort data into columns
    csvdata = data.T
    with open('SIRS_immunity_data2.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvtitle)
        writer.writerow(csvheader)
        writer.writerows(csvdata)
    
    # Make plot
    fig, ax = plt.subplots()
    ax.errorbar(immune_frac_array, infected_means[0], yerr=infected_sems[0], fmt='g.', ecolor='k', capsize=3)
    ax.set_xlabel('Immune fraction')
    ax.set_ylabel('Mean infected fraction')
    plt.show()
    
   
    
main()