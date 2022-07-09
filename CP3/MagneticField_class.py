"""
Same form as Poisson eqn.
Differential eqn. for magnetic vector potential of point wire
Invariance along z for infinite wire means we can use a 2D
lattice in fixed z-plane

Can use three different algorithms:
    Jacobi
    Gauss-Seidel
    Gauss-Seidel with successive over-relaxation (SOR)
"""

import numpy as np

# 2D lattice
class MagneticField_lattice3D:
    
    def __init__(self, N, threshold, algorithm, omega=1):
        self.N = N
        self.threshold = threshold
        self.algorithm = algorithm
        self.omega = omega
        self.Jz = np.zeros((self.N, self.N), dtype=np.int8)
        self.Jz[self.N//2, self.N//2] = 1
        self.Az = np.zeros((self.N, self.N), dtype=float)
        self.Az[0] = self.Az[self.N-1] = 0
        self.Az[:,0] = self.Az[:,self.N-1] = 0
    
    def update_Jacobi(self):
        self.Az = (1./4) * ( np.roll(self.Az, -1, axis = 0) + np.roll(self.Az, +1, axis = 0)
                           + np.roll(self.Az, -1, axis = 1) + np.roll(self.Az, +1, axis = 1)
                           + self.Jz)
        
        self.Az[0] = self.Az[self.N-1] = 0
        self.Az[:,0] = self.Az[:,self.N-1] = 0
        
    def update_GaussSeidel(self):
        for i in range(1,self.N-1):
            for j in range(1,self.N-1):
                self.Az[i,j] = (1./4) * ( self.Az[i+1, j] + self.Az[i-1, j]
                                        + self.Az[i, j+1] + self.Az[i, j-1]
                                        + self.Jz[i,j])
    
    def update_GausSeidelSOR(self):
        prev_Az = np.copy(self.Az)
        for i in range(1,self.N-1):
            for j in range(1,self.N-1):
                self.Az[i,j] = (self.omega*(1./4) * ( self.Az[i+1, j] + self.Az[i-1, j]
                                                        + self.Az[i, j+1] + self.Az[i, j-1]
                                                        + self.Jz[i,j])
                                  + (1-self.omega)*prev_Az[i,j])
        
    # Magnetic field expression given in recording 9    
    def calc_B_field(self):
        Bx = (1./2) * (np.roll(self.Az, -1, axis = 1) - np.roll(self.Az, +1, axis = 1))
        By = (-1./2) * (np.roll(self.Az, -1, axis = 0) - np.roll(self.Az, +1, axis = 0))
        return Bx, By        
    
    def play_simulation(self):
        if self.algorithm == 'Jacobi':
            update = self.update_Jacobi
        elif self.algorithm == 'Gauss-Seidel':
            update = self.update_GaussSeidel
        elif self.algorithm == 'Gauss-SeidelSOR':
            update = self.update_GausSeidelSOR
        prev_Az = np.copy(self.Az)
        update()
        error = np.sum(np.abs(self.Az - prev_Az))
        while error >= self.threshold:
            prev_Az = np.copy(self.Az)
            update()
            error = np.sum(np.abs(self.Az - prev_Az))
        Bx, By = self.calc_B_field()
        return self.Az, Bx, By
    
    def count_iterations(self):
        if self.algorithm == 'Jacobi':
            update = self.update_Jacobi
        elif self.algorithm == 'Gauss-Seidel':
            update = self.update_GaussSeidel
        elif self.algorithm == 'Gauss-SeidelSOR':
            update = self.update_GausSeidelSOR
        prev_Az = np.copy(self.Az)
        update()
        error = np.sum(np.abs(self.Az - prev_Az))
        num_iterations = 1
        while error >= self.threshold:
            prev_Az = np.copy(self.Az)
            update()
            num_iterations += 1
            error = np.sum(np.abs(self.Az - prev_Az))
        return num_iterations
        
        