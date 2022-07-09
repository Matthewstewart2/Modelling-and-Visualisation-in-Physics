import matplotlib
matplotlib.use('TKAgg')
import random
import numpy as np
import matplotlib.pyplot as plt

#
class Lattice2D(object):
    #
    def __init__(self, lx, ly, temp, dynamics, start_spins):
        self.J = 1.
        self.nstep = 10100
        self.lx = lx
        self.ly = ly
        self.temp = temp
        self.dynamics = dynamics
        self.spins = start_spins
        self.M = self.calc_M()
        self.E = self.calc_E()
        if self.dynamics == '1':
            self.absMtot = 0.
            self.Mtot = 0.
            self.Mtot2 = 0.
        self.Etot = 0.
        self.Etot2 = 0.
        
    #
    def calc_M(self):
        return np.sum(self.spins)
    
    #
    def calc_E(self):
        E_lat = 0
        for i in range(self.lx):
            for j in range(self.ly):
                E_lat += -self.J * self.spins[i][j] * (self.spins[i-1][j] + self.spins[i][j-1])
        return E_lat
        
    #    
    def update_glauber(self):
        itrial=np.random.randint(0,self.lx)
        jtrial=np.random.randint(0,self.ly)
        delta_E = self.calc_delta_E(itrial, jtrial)
        if delta_E <= 0 or random.random() <= np.exp(-delta_E / self.temp):
            self.spins[itrial,jtrial] *= -1
            self.M += 2*self.spins[itrial,jtrial]
            self.E += delta_E

    #    
    def update_kawasaki(self):
        itrial1=np.random.randint(0,self.lx)
        jtrial1=np.random.randint(0,self.ly)
        itrial2=np.random.randint(0,self.lx)
        jtrial2=np.random.randint(0,self.ly)
        while itrial1 == itrial2 and jtrial1 == jtrial2:
            itrial1=np.random.randint(0,self.lx)
            jtrial1=np.random.randint(0,self.ly)
            itrial2=np.random.randint(0,self.lx)
            jtrial2=np.random.randint(0,self.ly)
        if self.spins[itrial1,jtrial1] == self.spins[itrial2,jtrial2]:
            return
        delta_E = self.calc_delta_E(itrial1, jtrial1) + self.calc_delta_E(itrial2, jtrial2)
        if ((abs(itrial1 - itrial2) + abs(jtrial1 - jtrial2) == 1)
            or (itrial1 == itrial2 and abs(jtrial1 - jtrial2) == self.ly - 1)
            or (jtrial1 == jtrial2 and abs(itrial1 - itrial2) == self.lx - 1)):
            delta_E += 4*self.J
        if delta_E <= 0 or random.random() <= np.exp(-delta_E / self.temp):
            self.spins[itrial1,jtrial1] *= -1
            self.spins[itrial2,jtrial2] *= -1
            self.E += delta_E

    #        
    def calc_delta_E(self, itrial, jtrial):
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
        E_cont = -self.J * self.spins[itrial,jtrial] * (self.spins[itrial,next_j] +
                                                        self.spins[itrial,prev_j] +
                                                        self.spins[next_i,jtrial] +
                                                        self.spins[prev_i,jtrial])
        delta_E = -2 * E_cont
        return delta_E

    #    
    def play_simulation(self, animate=True, ct_sweeps=10, ss_sweeps=100):
        if animate:
            fig = plt.figure()
            im=plt.imshow(self.spins, animated=True)
        mc_steps = (self.nstep-ss_sweeps)/ct_sweeps
        if self.dynamics == '1':
            update = self.update_glauber
            Ms_array = np.zeros(mc_steps)
        else:
            update = self.update_kawasaki
        Es_array = np.zeros(mc_steps)
        for n in range(self.nstep):
            for i in range(self.lx):
                for j in range(self.ly):
                    update()
            if n%1==0: 
                if animate:
                    plt.cla()
                    im=plt.imshow(self.spins, animated=True, cmap='coolwarm', vmin=-1, vmax=1)
                    plt.draw()
                    plt.pause(0.0001)               
            if n >= ss_sweeps and n%ct_sweeps == 0:
                if self.dynamics == '1':
                    self.absMtot += abs(self.M)
                    self.Mtot += self.M
                    self.Mtot2 += (self.M)**2
                self.Etot += self.E
                self.Etot2 += (self.E)**2
        
        mc_steps = (self.nstep-ss_sweeps)/ct_sweeps
        if self.dynamics == '1':            
            avg_absM = self.absMtot / mc_steps
            avg_M = self.Mtot / mc_steps
            avg_M2 = self.Mtot2 / mc_steps
            suscept = (1./(self.lx*self.ly*self.temp))*(avg_M2 - avg_M**2)
        avg_E = self.Etot / mc_steps
        avg_E2 = self.Etot2 / mc_steps
        heat_cap = (1./(self.lx*self.ly*self.temp**2))*(avg_E2 - avg_E**2)
        
        if self.dynamics == '1':
            return avg_absM, avg_E, suscept, heat_cap, self.spins
        else:
            return avg_E, heat_cap, self.spins
    
    
    
    
    
    