"""
Solving initial value problem Cahn-Hilliard eqn. on 2D lattice

Can be animated
Can generate history of free energy
"""

import matplotlib
matplotlib.use('TKAgg')
import random
import numpy as np
import matplotlib.pyplot as plt

# 2D lattice
class CahnHilliard_lattice2D:
    
    def __init__(self, a, M, k, N, phi0, dx, dt):
        self.a = a
        self.M = M
        self.k = k
        self.N = N
        self.phi0 = phi0
        self.dx = dx
        self.dt = dt
        # Set initial state to phi0 plus noise
        self.phis = np.full((self.N, self.N), phi0)
        noise = 0.1
        self.phis += np.random.uniform(low=-noise, high=noise, size=(self.N, self.N))
        self.mus = self.calc_mus()
        
    # Calculate chemical potential mu    
    def calc_mus(self):
        # Using np.roll for periodic boundary conditions
        return (-self.a * self.phis + self.a * self.phis**3
                - (self.k/self.dx**2) * (np.roll(self.phis, -1, axis = 0)
                                          + np.roll(self.phis, +1, axis = 0)
                                          + np.roll(self.phis, -1, axis = 1)
                                          + np.roll(self.phis, +1, axis = 1)
                                          - 4 * self.phis)
               )
    
    # Calculate free energy density with expression from notes
    def calc_free_energy_density(self):
        return (-self.a / 2 * self.phis**2 + self.a / 4 * self.phis**4
                + self.k / (8*self.dx**2) * ((np.roll(self.phis, -1, axis = 0)
                                            - np.roll(self.phis, +1, axis = 0))**2
                                            +(np.roll(self.phis, -1, axis = 1)
                                            - np.roll(self.phis, +1, axis = 1))**2)
               )
    
    
    # Update rule from notes
    def update(self):
        self.phis += (self.M * self.dt) / self.dx**2 * (np.roll(self.mus, -1, axis = 0)
                                                      + np.roll(self.mus, +1, axis = 0)
                                                      + np.roll(self.mus, -1, axis = 1)
                                                      + np.roll(self.mus, +1, axis = 1)
                                                      - 4 * self.mus)
        self.mus = self.calc_mus()
        
    # PLay the simulation
    def play_simulation(self, animate=True, num_frames=int(1e6)):
        if animate:
            # Make figure if animating
            fig = plt.figure()
            #im = plt.imshow(self.phis, animated=True, cmap='coolwarm', vmin=-1., vmax=1.)
            plt.colorbar()
            # Run for a set number of frames
            for i in range(num_frames):
                self.update()
                # Animate every 100th
                if i == 10:
                    plt.cla()
                    im = plt.imshow(self.phis, animated=True, cmap='coolwarm', vmin=-1., vmax=1.)
                    plt.draw()
                    plt.pause(0.0001)
                    #if i == 10:
                    #    plt.savefig('part_a_snapshot')
        # If not animating, do the free energy experiment
        else:
            free_energies = []
            frames = []
            for i in range(num_frames):
                self.update()
                if i % 100 == 0:
                    frames.append(i)
                    print(i)
                    # Sum free energy density over lattice to get free energy
                    free_energies.append(np.sum(self.calc_free_energy_density()))
            return frames, free_energies
            
        
