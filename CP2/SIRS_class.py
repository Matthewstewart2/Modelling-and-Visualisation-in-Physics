"""
2D SIRS model lattice class
periodic boundary conditions

Can be animated, and calculate mean infected fraction and variance
"""

import matplotlib
matplotlib.use('TKAgg')
import random
import numpy as np
import matplotlib.pyplot as plt

# 2D lattice of sites
class SIRS_lattice2D:
    
    def __init__(self, N, p1, p2, p3, immune_frac=0):
        # N is side length of lattice so there are NxN sites in total
        self.N = N
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        # states [S, I, R]
        states = [0, 1, 2]
        # Random initial configuration
        self.population = np.random.choice(states, size=(self.N, self.N))
        # For special immunity experiment
        if immune_frac > 0:
            for i in range(self.N):
                for j in range(self.N):
                    r = random.random()
                    # With probability = immune fraction
                    if r <= immune_frac:
                        # New state 3 for 'immune' ie. permanently recovered
                        self.population[i, j] = 3 
        
    # Returns number of infected sites
    def mean_infected(self):
        return np.sum(self.population[self.population == 1])
  
    # Attempt tto update a single site
    def update(self):
        # Pick a random candidate site
        i = np.random.randint(0, self.N)
        j = np.random.randint(0, self.N)
        # Update rules given in notes
        if self.population[i, j] == 0:
            # Special cases to account for periodic boundary conditions
            if i == self.N - 1:
                i_next = 0
            else:
                i_next = i + 1
            i_prev = i - 1
            if j == self.N - 1:
                j_next = 0
            else:
                j_next = j + 1
            j_prev = j - 1
            # If any of nearest neighbours are infected there is a chance of S -> I for candidate site
            if 1 in [self.population[i, j_prev], self.population[i, j_next],
                     self.population[i_prev, j], self.population[i_next, j]] and random.random() <= self.p1:
                self.population[i, j] = 1
        # Chance for I -> R
        elif self.population[i, j] == 1:
            if random.random() <= self.p2:
                self.population[i, j] = 2
        # Chance for R -> S
        elif self.population[i, j] == 2:
            if random.random() <= self.p3:
                self.population[i, j] = 0
        # Note immune sites are never affected by update but can be chosen as candidates
    
    # Calculate variance of number of infected sites per site
    def calc_infected_variance(self, I_data, get_error):
        true_variance = (1./(self.N**2))*(np.mean(I_data**2) - np.mean(I_data)**2)
        if not get_error:
            return true_variance
        # Can choose to calculate error using bootstrap method
        else:
            num_resamples = 1000
            resampled_variance = np.zeros(num_resamples)
            for i in range(num_resamples):
                # Resample but the same values can be sampled multiple times
                new_I_data = np.random.choice(I_data, size=np.size(I_data))
                new_variance = (1./(self.N**2))*(np.mean(new_I_data**2) - np.mean(new_I_data)**2)
                resampled_variance[i] = new_variance
            # Error is standard deviation of distribution of respampled variances
            bootstrap_error = np.std(resampled_variance, ddof=1)
            return true_variance, bootstrap_error     
    
    # Play the simulation
    def play_simulation(self, animate=True, get_error=False):
        # Always 100 sweeps to reach steady state
        sweeps_eq = 100
        # Used 1000 sweeps for measurement apart from slice plot to find phase transition,
        # in which case 10000 was used
        n_sweeps = 1000
        if animate:
            # Make figure if animating
            fig = plt.figure()
            im = plt.imshow(self.population, animated=True, cmap='jet', vmin=0, vmax=2)
            plt.colorbar()
            for n in range(n_sweeps):
                for i in range(self.N * self.N):
                    self.update()
                if n % 4 == 0:
                    # Animate every 4 sweeps
                    plt.cla()
                    im = plt.imshow(self.population, animated=True, cmap='jet', vmin=0, vmax=2)
                    plt.draw()
                    plt.pause(0.0001)
        # If not animating, record values            
        else:
            num_infecteds = np.zeros(n_sweeps - sweeps_eq)
            # Time to reach steady state
            for n in range(sweeps_eq):
                for i in range(self.N * self.N):
                    self.update()
            # Now take measurements
            for n in range(n_sweeps - sweeps_eq):
                for i in range(self.N * self.N):
                    self.update()
                num_infecteds[n] = self.mean_infected()
            mean_infecteds = np.mean(num_infecteds)
            return mean_infecteds / (self.N)**2, self.calc_infected_variance(num_infecteds, get_error)                    
                
            