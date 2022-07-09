"""
B113446

Absorption time experiment
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
    
    absorption_times = []
    num_experiments = 10
    while len(absorption_times) < num_experiments:
        a_start = np.random.uniform(0., 1./3, (N,N))
        b_start = np.random.uniform(0., 1./3, (N,N))
        c_start = np.random.uniform(0., 1./3, (N,N))
        Simulation = ExamLattice2D(D, q, p, N, dx, dt, a_start, b_start, c_start)
        absorption_time = Simulation.absorption_time()
        if not np.isnan(absorption_time):
            absorption_times.append(absorption_time)
        
    # Write data to csv file
    csvtitle = ['# Absorption times']
    csvheader = ['Absorption times']
    # Transpose to sort data into columns
    csvdata = np.array([absorption_times]).T
    with open('Absorption_times.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvtitle)
        writer.writerow(csvheader)
        writer.writerows(csvdata)
        
    print('Mean absorption time =', np.mean(np.array(absorption_times)))
    print('Standard error of the mean =', np.std(np.array(absorption_times), ddof=1) / np.sqrt(10))
    
main()