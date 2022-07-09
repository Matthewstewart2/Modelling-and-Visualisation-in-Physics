"""
2D Conway's Game of Life simulation
periodic boundary conditions

Must specify system size and, optionally, special initial conditions

Can be animated, or conduct one of two experiments:
- get distribution of times to reach steady state
- measure glider centre of mass as function of time

writes data to a file
"""

from Game_of_life_class import GOL_lattice2D
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    # Remind user of correct command line arguments if needed
    if not(1 < len(sys.argv) < 4):
        print ("Usage python Game_of_life_play.py N (optional:glider/blinker)")
        sys.exit()
    N = int(sys.argv[1])
    if len(sys.argv) == 3:
        start_config = str(sys.argv[2])
        Simulation = GOL_lattice2D(N, start_config)
    else:
        start_config = 0
        Simulation = GOL_lattice2D(N)
    # Can choose to animate
    if input('Animate? (y/n): ') == 'y':
        animate = True
        Simulation.play_simulation(animate)
    # If not animating, do an experiment and collect data
    # Collect steady state time data experiment
    elif start_config == 0:
        animate = False
        num_experiments = 500
        ss_times = np.zeros(num_experiments)
        for i in range(len(ss_times)):
            Simulation = GOL_lattice2D(N)
            # Collect one time per experiment, could be nan if stuck in oscillating state
            ss_times[i] = Simulation.play_simulation(animate)
            # To check how long is left to go
            print('Done {}, ss_time = {}'.format(i+1, ss_times[i]))
        # Write to csv file
        csvtitle = ['# Conway\'s Game of Life Steady State Times']
        csvheader = ['Time']
        # Transpose to sort data into columns
        csvdata = np.array([ss_times]).T
        with open('GOL_ss_times.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csvtitle)
            writer.writerow(csvheader)
            writer.writerows(csvdata)
    # Glider speed experiment
    elif start_config == 'glider':
        animate = False
        Simulation = GOL_lattice2D(N, start_config)
        frames, x_coms, y_coms = Simulation.play_simulation(animate)
        csvtitle = ['# Conway\'s Game of Life Glider Centre of Mass']
        csvheader = ['Time', 'x_com', 'y_com']
        # Transpose to sort data into columns
        csvdata = np.array([frames, x_coms, y_coms]).T
        with open('GOL_glider_com.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csvtitle)
            writer.writerow(csvheader)
            writer.writerows(csvdata)
            
    
    
main()
    
    