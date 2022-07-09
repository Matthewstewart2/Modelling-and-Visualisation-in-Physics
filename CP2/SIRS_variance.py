"""
2D SIRS model phase diagram slice variance experiment
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
        print ("Usage python SIRS_variance.py N")
        sys.exit()
    N = int(sys.argv[1])
    # Zoom in to phase diagram slice from p1 =  0.2 to 0.5
    start = 0.2
    stop = 0.5
    num_pts = 31
    p1s = np.linspace(start, stop, num_pts)
    # Fix p2 = p3 = 0.5
    p2 = 0.5
    p3 = 0.5
    variance_array = np.zeros(len(p1s))
    variance_errors = np.zeros(len(p1s))
    for i in range(len(p1s)):
        Simulation = SIRS_lattice2D(N, p1s[i], p2, p3)
        # This time get the bootstrap errors on the variance
        mean_infected, variance = Simulation.play_simulation(animate=False, get_error=True)
        variance_array[i], variance_errors[i] = variance
        print('done', p1s[i])
            
    csvtitle = ['# SIRS model variance data p2 = p3 = 0.5']
    csvheader = ['p1', 'variance_I', 'variance_I_error']
    # Transpose to sort data into columns
    csvdata = np.array([p1s, variance_array, variance_errors]).T
    with open('SIRS_variance_data.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvtitle)
        writer.writerow(csvheader)
        writer.writerows(csvdata)
    
    # Plot with errorbars
    fig, ax = plt.subplots()
    ax.errorbar(p1s, variance_array, yerr=variance_errors, fmt='r.', ecolor='k', capsize=3)
    ax.set_xlabel('p1')
    ax.set_ylabel('Variance of number of infected sites')
    plt.show()
    
   
    
main()