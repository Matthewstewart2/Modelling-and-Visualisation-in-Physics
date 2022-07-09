"""
B113446

Species fraction plots
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
    time_list, frac_1_list, frac_2_list, frac_3_list = Simulation.species_fraction()
    
    # Write data to csv file
    csvtitle = ['# Species fraction against time']
    csvheader = ['time, type 1 fraction, type 2 fraction, type 3 fraction']
    # Transpose to sort data into columns
    csvdata = np.array([time_list, frac_1_list, frac_2_list, frac_3_list]).T
    with open('ExamSpeciesFraction.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvtitle)
        writer.writerow(csvheader)
        writer.writerows(csvdata)
        
    # Plot free energy against time
    fig, ax = plt.subplots()
    ax.plot(time_list, frac_1_list, 'b.', label='type 1')
    ax.plot(time_list, frac_2_list, 'y.', label='type 2')
    ax.plot(time_list, frac_3_list, 'r.', label='type 3')
    ax.legend()
    ax.set_title('Species Fraction against time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Fraction')
    plt.show()
    
main()