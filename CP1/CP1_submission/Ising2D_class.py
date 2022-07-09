"""
2D Ising model lattice class with periodic boundary conditions

States chosen with probabilities given by Boltzmann distribution
by using Markov chain + Metropolis algorithm

Can be animated and can record values of:
    mean abs(magnetisation)
    mean energy
    heat capacity per spin
    susceptibility
"""

import matplotlib
matplotlib.use('TKAgg')
import random
import numpy as np
import matplotlib.pyplot as plt

# Represents the 2D lattice of spins
class Lattice2D(object):
    #
    def __init__(self, lx, ly, temp, dynamics, start_spins):
        # set J=1 for convenience
        self.J = 1.
        # total number of sweeps (100 to reach steady state then measurements every 10 for 1000 measurements) 
        self.nstep = 10100
        # lengths of each axis of lattice
        self.lx = lx
        self.ly = ly
        # effective temperature, really kT
        self.temp = temp
        # Glauber or Kawasaki
        self.dynamics = dynamics
        # initial state
        self.spins = start_spins
        # get initial magnetisation and energy
        self.M = self.calc_M()
        self.E = self.calc_E()
        
    # calculate magnetisation of entire lattice, M
    def calc_M(self):
        return np.sum(self.spins)
    
    # calculate energy of entire lattice using given Ising hamiltonian, E
    def calc_E(self):
        E_lat = 0
        for i in range(self.lx):
            for j in range(self.ly):
                # each adds only the North and West neighbour interaction to avoid double counting
                # also works with periodic BCs
                E_lat += -self.J * self.spins[i][j] * (self.spins[i-1][j] + self.spins[i][j-1])
        return E_lat
        
    # one attempted spin flip for Glauber dynamics
    def update_glauber(self):
        # random candidate spin (Markov)
        itrial=np.random.randint(0,self.lx)
        jtrial=np.random.randint(0,self.ly)
        delta_E = self.calc_delta_E(itrial, jtrial)
        # flips if energetically favourable or with Boltzmann probability (Metropolis)
        if delta_E <= 0 or random.random() <= np.exp(-delta_E / self.temp):
            self.spins[itrial,jtrial] *= -1
            # if spin is flipped update M and E
            self.M += 2*self.spins[itrial,jtrial]
            self.E += delta_E

    # one attempted spin swap for Kawasaki dynamics 
    def update_kawasaki(self):
        # two random candidate spin
        itrial1=np.random.randint(0,self.lx)
        jtrial1=np.random.randint(0,self.ly)
        itrial2=np.random.randint(0,self.lx)
        jtrial2=np.random.randint(0,self.ly)
        # do it again if it chose the same spin twice
        while itrial1 == itrial2 and jtrial1 == jtrial2:
            itrial1=np.random.randint(0,self.lx)
            jtrial1=np.random.randint(0,self.ly)
            itrial2=np.random.randint(0,self.lx)
            jtrial2=np.random.randint(0,self.ly)
        # if the two spins are alligned, no need to update anything
        if self.spins[itrial1,jtrial1] == self.spins[itrial2,jtrial2]:
            return
        delta_E = self.calc_delta_E(itrial1, jtrial1) + self.calc_delta_E(itrial2, jtrial2)
        # checking if spins are nearest neighbours is weird with periodic BCs
        if ((abs(itrial1 - itrial2) + abs(jtrial1 - jtrial2) == 1)
            or (itrial1 == itrial2 and abs(jtrial1 - jtrial2) == self.ly - 1)
            or (jtrial1 == jtrial2 and abs(itrial1 - itrial2) == self.lx - 1)):
            # if so the energy drop will be overesimated so correction here
            delta_E += 4*self.J
        if delta_E <= 0 or random.random() <= np.exp(-delta_E / self.temp):
            self.spins[itrial1,jtrial1] *= -1
            self.spins[itrial2,jtrial2] *= -1
            # no need to update M for Kawasaki
            self.E += delta_E

    # calculate change in enegry by flipping one spin       
    def calc_delta_E(self, itrial, jtrial):
        # get indices of nearest neighbours accounting for periodic BCs
        prev_i = itrial - 1
        prev_j = jtrial - 1
        if itrial != self.lx - 1:
            next_i = itrial + 1
        else:
            next_i = 0
        if jtrial != self.ly - 1:
            next_j = jtrial + 1
        else:
            next_j = 0
        # contribution to E the spin makes before flip
        E_cont = -self.J * self.spins[itrial,jtrial] * (self.spins[itrial,next_j] +
                                                        self.spins[itrial,prev_j] +
                                                        self.spins[next_i,jtrial] +
                                                        self.spins[prev_i,jtrial])
        # spin flip
        delta_E = -2 * E_cont
        return delta_E
    
    # returns a mean and standard error on the mean (SEM) for an array of data
    def mean_with_sem(self, data_array):
        data_mean = np.mean(data_array)
        data_sem = np.std(data_array, ddof=1) / np.sqrt(np.size(data_array))
        return (data_mean, data_sem)
    
    # return susceptibility with error from bootstrap resampling
    def suscept_with_bootstrap(self, Mdata_array, num_resamples=1000):
        true_suscept = (1./(self.lx*self.ly*self.temp))*(np.mean(Mdata_array**2) - np.mean(Mdata_array)**2)
        resampled_suscepts = np.zeros(num_resamples)
        # resample num_resamples times
        for i in range(num_resamples):
            # resample a dataset of same length but can choose same points multiple times
            new_Mdata_array = np.random.choice(Mdata_array, size=np.size(Mdata_array))
            new_suscept = (1./(self.lx*self.ly*self.temp))*(np.mean(new_Mdata_array**2) - np.mean(new_Mdata_array)**2)
            resampled_suscepts[i] = new_suscept
        # error is standard deviation of new distribution of resamped susceptibilities
        bootstrap_error = np.std(resampled_suscepts, ddof=1)
        return (true_suscept, bootstrap_error)

    # same for heat capacity per spin just rewritten for factor of T difference between equations
    def heat_cap_with_bootstrap(self, Edata_array, num_resamples=1000):
        true_heat_cap = (1./(self.lx*self.ly*self.temp**2))*(np.mean(Edata_array**2) - np.mean(Edata_array)**2)
        resampled_heat_caps = np.zeros(num_resamples)
        for i in range(num_resamples):
            new_Edata_array = np.random.choice(Edata_array, size=np.size(Edata_array))
            new_heat_cap = (1./(self.lx*self.ly*self.temp**2))*(np.mean(new_Edata_array**2) - np.mean(new_Edata_array)**2)
            resampled_heat_caps[i] = new_heat_cap
        bootstrap_error = np.std(resampled_heat_caps, ddof=1)
        return (true_heat_cap, bootstrap_error)
            
    # runs simulations for nsteps sweeps
    def play_simulation(self, animate=True, ct_sweeps=10, ss_sweeps=100):
        # if animating make figure and use imshow
        if animate:
            fig = plt.figure()
            im=plt.imshow(self.spins, animated=True)
        # how many points will be in Monte Carlo averages ie how many data points will be recorded
        mc_steps = int((self.nstep-ss_sweeps)/ct_sweeps)
        # choose update rule
        if self.dynamics == '1':
            update = self.update_glauber
            # only need to record M with Glauber
            Ms_array = np.zeros(mc_steps)
        else:
            update = self.update_kawasaki
        Es_array = np.zeros(mc_steps)
        data_counter = 0
        # definition of one sweep is lx*ly attempted spin flips
        for n in range(self.nstep):
            for i in range(self.lx):
                for j in range(self.ly):
                    update()
            # animate every sweep looks good but takes longer to reach equilibrium steady state
            if n%1==0: 
                if animate:
                    plt.cla()
                    im=plt.imshow(self.spins, animated=True, cmap='coolwarm', vmin=-1, vmax=1)
                    plt.draw()
                    plt.pause(0.0001)
            # wait until in equilibrium steady state
            # then take measurements every 10 sweeps for uncorrelated data
            if n >= ss_sweeps and n%ct_sweeps == 0:
                # can't just keep running total, have to keep history to use bootstrap resampling
                if self.dynamics == '1':
                    Ms_array[data_counter] = self.M
                Es_array[data_counter] = self.E
                data_counter += 1 
        # calculate moments with errors
        if self.dynamics == '1':     
            absMs_array = abs(Ms_array)
            avg_absM = self.mean_with_sem(absMs_array)
            suscept = self.suscept_with_bootstrap(Ms_array)
        avg_E = self.mean_with_sem(Es_array)
        heat_cap = self.heat_cap_with_bootstrap(Es_array)
        # return measurements for plotting
        if self.dynamics == '1':
            return avg_absM, avg_E, suscept, heat_cap, self.spins
        else:
            return avg_E, heat_cap, self.spins
    
    
    
    
    
    