"""
B113446

Animation
"""

from B113446_exam_class import ExamLattice2D
import sys
import numpy as np

def main():
    # Remind user of correct command line arguments if needed
    if(len(sys.argv) != 7):
        print ("Usage python B113446_exam_play.py D q p N dx dt")
        sys.exit()
    # Input the various constants of choice
    D = float(sys.argv[1])
    q = float(sys.argv[2])
    p = float(sys.argv[3])
    N = int(sys.argv[4])
    dx = float(sys.argv[5])
    dt = float(sys.argv[6])
    a_start = np.random.uniform(0., 1./3, (N,N))
    b_start = np.random.uniform(0., 1./3, (N,N))
    c_start = np.random.uniform(0., 1./3, (N,N))
    Simulation = ExamLattice2D(D, q, p, N, dx, dt, a_start, b_start, c_start)
    Simulation.play_simulation()
    
main()