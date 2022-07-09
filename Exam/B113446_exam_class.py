"""
B113446
"""

import matplotlib
matplotlib.use('TKAgg')
import random
import numpy as np
import matplotlib.pyplot as plt

# 2D lattice
class ExamLattice2D:
    
    def __init__(self, D, q, p, N, dx, dt, a_start, b_start, c_start):
        # parameters from paper
        self.D = D
        self.q = q
        self.p = p
        self.N = N
        self.dx = dx
        self.dt = dt
        self.a_field = a_start
        self.b_field = b_start
        self.c_field = c_start
        self.tau_field = np.zeros(self.a_field.shape)
        self.calc_tau_field()
    
    # calculate type field
    def calc_tau_field(self):
        remain_field = np.ones(self.a_field.shape) - self.a_field - self.b_field - self.c_field
        for i in range(self.a_field.shape[0]):
            for j in range(self.a_field.shape[1]):
                self.tau_field[i, j] = np.argmax(np.array([remain_field[i, j],
                                                           self.a_field[i, j],
                                                           self.b_field[i, j],
                                                           self.c_field[i, j]]))
        

    # update all three concentrations simulataneously
    def update(self):
        # use copies of initial concentrations so update are synchronised
        temp_a = np.copy(self.a_field)
        temp_b = np.copy(self.b_field)
        temp_c = np.copy(self.c_field)
        
        self.a_field = temp_a + self.dt*((self.D / self.dx**2) * (np.roll(temp_a, -1, axis = 0)
                                                                + np.roll(temp_a, +1, axis = 0)
                                                                + np.roll(temp_a, -1, axis = 1)
                                                                + np.roll(temp_a, +1, axis = 1)
                                                                - 4 * temp_a)
                              + self.q*temp_a*(np.ones(temp_a.shape)-temp_a-temp_b-temp_c)
                              - self.p*temp_a*temp_c)
        
        self.b_field = temp_b + self.dt*((self.D / self.dx**2) * (np.roll(temp_b, -1, axis = 0)
                                                                + np.roll(temp_b, +1, axis = 0)
                                                                + np.roll(temp_b, -1, axis = 1)
                                                                + np.roll(temp_b, +1, axis = 1)
                                                                - 4 * temp_b)
                              + self.q*temp_b*(np.ones(temp_a.shape)-temp_a-temp_b-temp_c)
                              - self.p*temp_a*temp_b)
        
        self.c_field = temp_c + self.dt*((self.D / self.dx**2) * (np.roll(temp_c, -1, axis = 0)
                                                                + np.roll(temp_c, +1, axis = 0)
                                                                + np.roll(temp_c, -1, axis = 1)
                                                                + np.roll(temp_c, +1, axis = 1)
                                                                - 4 * temp_c)
                              + self.q*temp_c*(np.ones(temp_a.shape)-temp_a-temp_b-temp_c)
                              - self.p*temp_b*temp_c)
        self.calc_tau_field()
        
    # PLay the simulation
    def play_simulation(self, animate=True, num_frames=int(1e6)):
        if animate:
            # Make figure if animating
            fig = plt.figure()
            im = plt.imshow(self.tau_field, animated=True, cmap='jet', vmin=0, vmax=3)
            plt.colorbar()
            # Run for a set number of frames
            for i in range(num_frames):
                self.update()
                # Animate every 10th
                if i % 10==0:
                    plt.cla()
                    im = plt.imshow(self.tau_field, animated=True, cmap='jet', vmin=0, vmax=3)
                    plt.draw()
                    plt.pause(0.0001)
                    
    # Species fraction experiment
    def species_fraction(self, num_frames=int(2e3)):
        frac_1_list = []
        frac_2_list = []
        frac_3_list = []
        time_list = []
        for i in range(num_frames):
            frac_1 = (self.tau_field == 1).sum() / self.N**2
            frac_1_list.append(frac_1)
            frac_2 = (self.tau_field == 2).sum() / self.N**2
            frac_2_list.append(frac_2)
            frac_3 = (self.tau_field == 3).sum() / self.N**2
            frac_3_list.append(frac_3)
            time_list.append(self.dt * i)
            self.update()
            # Just to check progress
            print(float(i) / num_frames)
        return time_list, frac_1_list, frac_2_list, frac_3_list
    
    # Absorption time experiment
    def absorption_time(self):
        frac_1 = (self.tau_field == 1).sum() / self.N**2
        frac_2 = (self.tau_field == 2).sum() / self.N**2
        frac_3 = (self.tau_field == 3).sum() / self.N**2
        frame = 0
        while True:
            if (frac_1 == 1. or frac_2 == 1. or frac_3 == 1.):
                return frame * self.dt
            # As instructed stop if still going at time of 1000
            elif frame * self.dt >= 1000:
                return np.nan
            self.update()
            frac_1 = (self.tau_field == 1).sum() / self.N**2
            frac_2 = (self.tau_field == 2).sum() / self.N**2
            frac_3 = (self.tau_field == 3).sum() / self.N**2
            frame += 1
            
    # Oscillations experiment
    def oscillations(self, num_frames=int(1e4)):
        a1_list = []
        a2_list = []
        time_list = []
        for i in range(num_frames):
            a1_list.append(self.a_field[0,0])
            a2_list.append(self.a_field[self.N//2, self.N//2])
            time_list.append(self.dt * i)
            self.update()
            print(float(i) / num_frames)
        return time_list, a1_list, a2_list
        
        
        
        
        
        
        
        
        
        
        