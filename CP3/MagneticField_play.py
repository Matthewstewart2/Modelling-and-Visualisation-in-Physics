"""
Solving for magnetic vector potential z component and magnetic field
"""

from MagneticField_class import MagneticField_lattice3D
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    # Remind user of correct command line arguments if needed
    if(len(sys.argv) != 3):
        print ("Usage python MagneticField_play.py N threshold")
        sys.exit()
    N = int(sys.argv[1])
    threshold = float(sys.argv[2])
    print('Choose algorithm:')
    print('1 for Jacobi')
    print('2 for Gauss-Seidel')
    print('3 for Gauss-Seidel with successive over-relaxation')
    print('')
    algorithm = input()
    if algorithm == '1':
        algorithm = 'Jacobi'
        omega = 1
    elif algorithm == '2':
        algorithm = 'Gauss-Seidel'
        omega = 1
    elif algorithm == '3':
        algorithm = 'Gauss-SeidelSOR'
        omega = float(input('Choose omega between 0 and 2: '))
    Simulation = MagneticField_lattice3D(N, threshold, algorithm, omega)
    Az, Bx, By = Simulation.play_simulation()
    
    fig, ax = plt.subplots(1, 2)
    fig.suptitle('Midplane {} Algorithm'.format(algorithm))
    pos = ax[0].imshow(Az, cmap='hot', origin='lower') 
    ax[0].set_title(r'$A_z$')
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')
    fig.colorbar(pos, ax=ax[0])
    magnitudes = np.sqrt(Bx**2 + By**2)
    magnitudes[magnitudes == 0] = 1
    ax[1].quiver(By/magnitudes, Bx/magnitudes, scale=40)
    ax[1].set_title('B-field')
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('y')
    
    x_list = []
    y_list = []
    Az_list = []
    Bx_list = []
    By_list = []
    for i in range(len(Az)):
        for j in range(len(Az)):
            x_list.append(i)
            y_list.append(j)
            Az_list.append(Az[i,j])
            Bx_list.append(Bx[i,j])
            By_list.append(By[i,j])
    csvtitle = ['# Magnetic Field {} algorithm data'.format(algorithm)]
    csvheader = ['x', 'y', 'Az', 'Bx', 'By']
    # Transpose to sort data into columns
    csvdata = np.array([x_list, y_list, Az_list, Bx_list, By_list]).T
    with open('MagneticFieldData{}.csv'.format(algorithm), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvtitle)
        writer.writerow(csvheader)
        writer.writerows(csvdata)
        
    plt.show()

main()
                
                
                
                
                