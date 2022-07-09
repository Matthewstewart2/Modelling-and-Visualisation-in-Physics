"""
2D Conway's Game of Life lattice class
periodic boundary conditions

Can be animated, or conduct one of two experiments:
- get distribution of times to reach steady state
- measure glider centre of mass as function of time
"""

import matplotlib
matplotlib.use('TKAgg')
import random
import numpy as np
import matplotlib.pyplot as plt

# 2D lattice of cells
class GOL_lattice2D:
    
    def __init__(self, N, start_config=0):
        # Here N is SIDE LENGTH of lattice so number of cells is N^2
        self.N = N
        # Keywords 'glider' or 'blinker' give special initial conditions
        self.start_config = start_config
        self.cells = np.zeros((N,N),dtype=int)
        # Glider initial configuration
        if start_config == 'glider':
            # Make glider at centre of frame
            middle_idx = self.N // 2
            # Make glider shape from Fig. 1 (D) in notes
            self.cells[middle_idx][middle_idx - 1] \
            = self.cells[middle_idx + 1][middle_idx] \
            = self.cells[middle_idx - 1][middle_idx + 1] \
            = self.cells[middle_idx][middle_idx + 1] \
            = self.cells[middle_idx + 1][middle_idx + 1] \
            = 1
        # Blinker initial configuration    
        elif start_config == 'blinker':
            middle_idx = self.N // 2
            # Same as lecture recording demo
            self.cells[middle_idx - 1:middle_idx + 2, middle_idx - 3:middle_idx + 4] = 1
        # Otherwise make a random initial configuration
        else:
            for i in range(N):
                for j in range(N):
                    r = random.random()
                    if (r < 0.5):
                        self.cells[i, j] = 1
            
    # One iteration of a parallel (all cells at once) update scheme given in notes
    def update(self):
        new_cells = np.zeros((self.N,self.N),dtype=int)
        for i in range(self.N):
            for j in range(self.N):
                # Find neighbours with special cases to account for periodic BCs
                if i == self.N - 1:
                    i_prev = -2
                    i_next = 0
                else:
                    i_prev = i - 1
                    i_next = i + 1
                if j == self.N - 1:
                    j_prev = -2
                    j_next = 0
                else:
                    j_prev = j - 1
                    j_next = j + 1
                # array.take() just slices array but mode='wrap' accounts for periodic BCs
                # Slice array in both axes to make new 3x3 block centred on (i, j)
                # First condition accounts for both alive cell with 2 alive neighbours and dead cell with 3
                # Second condition allows possibility of alive cell with 3 alive neighbours
                if (np.sum(self.cells.take(range(i_prev,i_next+1),mode='wrap',axis=0) \
                           .take(range(j_prev,j_next+1), mode='wrap', axis = 1)) == 3
                    or (self.cells[i, j] == 1 and 
                        np.sum(self.cells.take(range(i_prev,i_next+1),mode='wrap',axis=0) \
                               .take(range(j_prev,j_next+1), mode='wrap', axis = 1)) == 4)):
                    new_cells[i, j] = 1
        # Scheme acts on frozen lattice at start of update so only now update all cells at once
        self.cells = new_cells
        
    # Returns x centre of mass (COM) and y COM from lattice with only glider on it
    def glider_com(self):
        # Get indices of living sites and zero elsewhere
        xs, ys = np.indices((self.N, self.N)) * self.cells
        x_com = np.sum(xs) / np.sum(self.cells)
        y_com = np.sum(ys) / np.sum(self.cells)
        # If object crosses boundaries, void this measurement
        if np.sum(self.cells[0]) !=0 and np.sum(self.cells[-1]) !=0:
            x_com = np.nan
        if np.sum(self.cells[:,0]) !=0 and np.sum(self.cells[:,-1]) !=0:
            y_com = np.nan
        return x_com, y_com
        
    # Runs the simulation, can choose to animate or do an experiment
    def play_simulation(self, animate=True):
        frame = 0
        if animate:
            # Make the figure
            fig = plt.figure()
            im=plt.imshow(self.cells, animated=True)        
            while True:
                # Animate each frame
                plt.cla()
                im = plt.imshow(self.cells, animated=True, cmap='coolwarm', vmin=0, vmax=1)
                plt.draw()
                plt.pause(0.01)
                self.update()
                frame += 1      
        else:
            # Steady state time experiment  
            if self.start_config == 0:
                # Candidate time to reach steady state (SS)
                ss_time = 0
                counter = 0
                nums_alive = np.sum(self.cells)
                while True:
                    # In blocks of 10 frames
                    if frame % 10 == 0:
                        # Make a first candidate ss time
                        if ss_time == 0:
                            ss_time = frame
                        # If number of alve cells hasn't changed by next block increment counter
                        if nums_alive == np.sum(self.cells):
                            counter += 1
                        # Otherwise reset the counter and take the new candidate ss time
                        else:
                            nums_alive = np.sum(self.cells)
                            counter = 0
                            ss_time = frame
                    # If after 10 blocks of 10 frames, number alive still unchanged,
                    # record candidate ss time in sweeps
                    if counter == 10:
                        return float(ss_time) / self.N**2
                    # If 2 sweeps is reached, assume it's stuck in an oscillating state and void the measurement
                    if frame == 2 * self.N**2:
                        return np.nan
                    self.update()
                    frame += 1
            # Glider speed experiment
            elif self.start_config == 'glider':
                # Choose reasonable number of frames over which to record COMs
                num_pts = 300
                x_coms = np.zeros(num_pts)
                y_coms = np.zeros(num_pts)
                for i in range(num_pts):
                    x_coms[i], y_coms[i] = self.glider_com()
                    self.update()
                    frame += 1
                # Record times in frames as well as COMs
                return np.array(list(range(num_pts))), x_coms, y_coms
                    
                            
                
            

