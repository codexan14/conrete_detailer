import core.materials as materials
import core.structural_sections as structural_sections
import core.geometry as geometry
import numpy as np
import matplotlib.pyplot as plt 
import numpy as np 
from numpy.typing import NDArray

def interaction_diagram(
        b: float, 
        h: float, 
        fc: float, 
        fy: float, 
        As_i: NDArray[np.float64], 
        y_i: NDArray[np.float64] = np.zeros(0), 
        Es: float = 200000,
        n: int = 10) -> None:
    """
    Plots the interaction diagram of a Reinforced Concrete Section

    Args:
        b (float): Width of the section.
        h (float): Height of the section.
        fc (float): Compression strength of the concrete.
        fy (float): Yield strength of the steel.
        As_i (np.array): List of rebar areas in a given position y_i
        y_i (np.array): List of rebar
        Es (float): Elastic modulus of the steel
        n (int): Number of points for the interaction diagram

    Returns:
        plt.figure
    """
    
    if len(y_i) == 0 or len(As_i) != len(y_i): # Defines the position, if not given or invalid

        # Available Lenght = Height - Cover - Stirrups Diameter - 2*Half Diameter #25 bar [mm]
        available_length: float = h - 40*2 - 2*10 - 2*12.5 

        # Center to Center Bar separation
        spacing: float = available_length/(len(As_i) - 1)

        y_i = np.array([40 + 10 + 12.50 + spacing*i for i in range(len(As_i))], dtype=np.float64)


    # Defines the length of the arrays where forces and moment will be contained
    nominal_force_i: NDArray[np.float64] = np.zeros(n)
    nominal_moment_i: NDArray[np.float64] = np.zeros(n)
    reduced_nominal_force_i: NDArray[np.float64] = np.zeros(n)
    reduced_nominal_moment_i: NDArray[np.float64] = np.zeros(n)

    # List of values of c for the interaction diagram.
    c_i = 5*h*np.logspace(0.01, 1, n, base=100, dtype=np.float64)/100 

    for i, c in enumerate(c_i): 
        # Deformation angle of the section
        theta: float = float(0.003/c)   

        #Whitney Compression block. Goes from 0 to h. The clip function ensures that.
        a: NDArray[np.float64] = np.clip(0.85*c, 0, h)

        # Calculation of the Force due to the deformation of the Concrete
        Cc = 0.85*fc*a*b 

        # Calculation of the Force due to the deformation of the Steel
        steel_strain_i: NDArray[np.float64] = theta*(c - y_i)
        steel_stress_i: NDArray[np.float64] = np.clip(steel_strain_array*Es, -fy, fy)
        steel_force_i = steel_stress_array * As_i

        F = Cc + np.sum(steel_force_array)
        M = Cc*(h/2 - a/2) + np.sum(steel_force_array*(h/2 - y_i))
        # print(F,M)

        es = steel_strain_array[-1]
        phi = np.clip(0.65 + (0.90-0.65)/(0.005-0.0021)*(-es-0.0021), 0.65, 0.90)

        phiMn = M*phi 
        phiF = phi*np.clip(F , -np.sum(As_i)*420,0.80*(0.85*fc*(b*h - np.sum(As_i)) + np.sum(As_i)*420))

        print(a, phi, es)
        nominal_force_i[i] = F/1000
        nominal_moment_i[i] = M/1000/1000

        reduced_nominal_moment_i[i] = phiMn/1000/1000
        reduced_nominal_force_i[i] = phiF/1000



    plt.plot(nominal_moment_i,nominal_force_i,'-o')
    plt.plot(reduced_nominal_moment_i, reduced_nominal_force_i, '-*')

    print(y_i)
    plt.show()


if __name__ == "__main__":
    interaction_diagram(
        b=400, 
        h=600, 
        fc=28, 
        fy=420,
        As_i = [507*4, 507*2, 507*2, 507*4],
        n = 50)