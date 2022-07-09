"""
B113446

Oscillation of two grid points
"""

from B113446_exam_class import ExamLattice2D
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    # Remind user of correct command line arguments if needed
    if(len(sys.argv) != 7):
        print ("Usage python B113446_exam_play.py D q p N dx dt")
        sys.exit()
    # Input the various constants of choice
    D = float(sys.argv[1])
    p = float(sys.argv[2])
    q = float(sys.argv[3])
    N = int(sys.argv[4])
    dx = float(sys.argv[5])
    dt = float(sys.argv[6])
    a_start = np.random.uniform(0., 1./3, (N,N))
    b_start = np.random.uniform(0., 1./3, (N,N))
    c_start = np.random.uniform(0., 1./3, (N,N))
    Simulation = ExamLattice2D(D, q, p, N, dx, dt, a_start, b_start, c_start)
    time_list, a1_list, a2_list = Simulation.oscillations()
    
    # Write data to csv file
    csvtitle = ['# Species fraction against time']
    csvheader = ['time, first a value, second a value']
    # Transpose to sort data into columns
    csvdata = np.array([time_list, a1_list, a2_list]).T
    with open('SpeciesOscillations.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvtitle)
        writer.writerow(csvheader)
        writer.writerows(csvdata)
        
    # Plot free energy against time
    fig, ax = plt.subplots()
    ax.plot(time_list, a1_list, 'b.', label='a1')
    ax.plot(time_list, a2_list, 'y.', label='a2')
    ax.legend()
    ax.set_title('Concentration of type a')
    ax.set_xlabel('Time')
    ax.set_ylabel('Concentration')
    plt.show()
    
main()