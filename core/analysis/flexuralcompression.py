import numpy as np
import numpy as np 
from typing import Callable
from numpy.typing import NDArray
from core.utils import numeric_solver, numeric_integration
import matplotlib.pyplot as plt

def beta_1(fc: float) -> float: 
    return min(0.85, max(0.65, 0.85 - 0.05*(fc - 28)/7)) 

def get_concrete_ultimate_force(fc: float, c: float, b: float) -> float: 
    return 0.85*fc*beta_1(fc)*c*b 

def get_concrete_force(fc: float, curvature: float, c: float, b: float) -> float: 
    stress: Callable[[float], float] = lambda x: curvature*x
    force: float = numeric_integration(stress, 0, c)
    return force


def steel_stress(steel_strain: float, fy: float, Es: float = 200000) -> float:
    return min(fy, max(-fy, steel_strain * Es)) 

def steel_stresses(steel_strains: list[float], fy: float, Es: float = 200000) -> list[float]: 
    return [steel_stress(strain, fy, Es) for strain in steel_strains]

def steel_force(rebar_areas: list[float], steel_stresses: list[float], fy: float, Es: float = 200000) -> float: 
    steel_forces: list[float] = [area * stress for area,stress in zip(rebar_areas, steel_stresses)]
    return sum(steel_forces)

def get_neutral_axis(
        b: float, 
        rebar_areas: list[float], 
        rebar_positions: list[float], 
        fc: float, 
        fy: float, 
        Es: float, 
        force: float,
        curvature: float) -> float: 
    """
    Gets the value of the neutral axis given hte curvature and force
    """
    s_strains: Callable[[float], list[float]] = lambda c: [(c - position)*curvature for position in rebar_positions]

    s_stresses: Callable[[float], list[float]] = lambda c: steel_stresses(s_strains(c), fy, Es)

    force_function: Callable[[float], float] = lambda c: get_concrete_ultimate_force(fc, c, b) + steel_force(rebar_areas, s_stresses(c), fy)
    force_goal: float = force 

    nutral_axis: float = numeric_solver(force_function, force_goal, 0, max(rebar_positions), 1e-10)
    
    return nutral_axis 

def get_moment_curvature(
        b: float, 
        rebar_areas: list[float], 
        rebar_positions: list[float], 
        fc: float, 
        fy: float, 
        Es: float,
        final_curvature: float = 0.001, 
        n: int = 10) -> tuple[list[float], list[float]]:
    
    curvatures: list[float] = ((np.logspace(start=0, stop=1, num=n, base=10)-1)/9*final_curvature).tolist()
    neutral_axes: list[float] = []

    for curvature in curvatures: 
        neutral_axis: float = get_neutral_axis(b, rebar_areas, rebar_positions, fc, fy, Es, force = 0, curvature=curvature)
        
        neutral_axes.append(neutral_axis)

    return curvatures, neutral_axes

def get_phi_nominal_force_and_moment(
        b: float, 
        h: float, 
        fc: float, 
        fy: float, 
        c: float,
        rebar_areas: NDArray[np.float64], 
        rebar_positions: NDArray[np.float64] = np.zeros(0), 
        Es: float = 200000) -> tuple[float, float, float]: 
    """
    Gets the value of phi, the nominal force and nominal moment given the neutral axis
    """

    theta: float = float(0.003/c)   

        #Whitney Compression block. Goes from 0 to h. The clip function ensures that.
    a: NDArray[np.float64] = np.clip(0.85*c, 0, h)

    # Calculation of the Force due to the deformation of the Concrete
    get_concrete_ultimate_force = 0.85*fc*a*b 

    # Calculation of the Force due to the deformation of the Steel
    steel_strains: NDArray[np.float64] = theta*(c - rebar_positions)
    steel_stresses: NDArray[np.float64] = np.clip(steel_strains*Es, -fy, fy)
    steel_forces = steel_stresses* rebar_areas

    phi = np.clip(0.65 + (0.90-0.65)/(0.005-0.0021)*(-steel_strains[-1]-0.0021), 0.65, 0.90)

    nominal_force = float(get_concrete_ultimate_force + np.sum(steel_forces))

    nominal_moment = float(get_concrete_ultimate_force*(h/2 - a/2) + np.sum(steel_forces*(h/2 - rebar_positions)))
    # print(F,M)

    return phi, nominal_force, nominal_moment

def interaction_diagram(
        b: float, 
        h: float, 
        fc: float, 
        fy: float, 
        rebar_areas: NDArray[np.float64], 
        rebar_positions: NDArray[np.float64] = np.zeros(0), 
        Es: float = 200000,
        n: int = 10) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Plots the interaction diagram of a Reinforced Concrete Section

    Args:
        b (float): Base of the concrete section
        h (float): Height of the concrete section 
        
        FINISH THIS DOC

    Returns:
        plt.figure
    """
    
    if len(rebar_positions) == 0 or len(rebar_areas) != len(rebar_positions): # Defines the position, if not given or invalid

        # Available Lenght = Height - Cover - Stirrups Diameter - 2*Half Diameter #25 bar [mm]
        available_length: float = h - 40*2 - 2*10 - 2*12.5 

        # Center to Center Bar separation
        spacing: float = available_length/(len(rebar_areas) - 1)

        rebar_positions = np.array([40 + 10 + 12.50 + spacing*i for i in range(len(rebar_areas))], dtype=np.float64)


    # Defines the length of the arrays where forces and moment will be contained
    nominal_forces: NDArray[np.float64] = np.zeros(n)
    nominal_moments: NDArray[np.float64] = np.zeros(n)
    reduced_nominal_forces: NDArray[np.float64] = np.zeros(n)
    reduced_nominal_moments: NDArray[np.float64] = np.zeros(n)

    # List of values of c for the interaction diagram.
    c_values = 5*h*np.logspace(0.01, 1, n, base=100, dtype=np.float64)/100 

    for i, c in enumerate(c_values): 
        
        phi, nominal_force, nominal_moment = get_phi_nominal_force_and_moment(
            b, h, fc, fy, float(c), rebar_areas, rebar_positions
        )

        reduced_nominal_moment = phi * nominal_moment 
        reduced_nominal_force = phi*np.clip(nominal_force , -np.sum(rebar_areas)*fy,0.80*(0.85*fc*(b*h - np.sum(rebar_areas)) + np.sum(rebar_areas)*420))

        nominal_forces[i] = nominal_force
        nominal_moments[i] = nominal_moment

        reduced_nominal_moments[i] = reduced_nominal_moment
        reduced_nominal_forces[i] = reduced_nominal_force

    return nominal_forces, nominal_moments, reduced_nominal_forces, reduced_nominal_moments


if __name__ == "__main__":
    result = get_neutral_axis(400, [507*2 + 126*2, 126*2, 126*2, 507*2+126*2], [80, 225, 375, 520], 28, 420, 200000, 10000, 0.001/600)
    k, M = get_moment_curvature(400, [507, 126, 126, 507], [80, 225, 375, 520], 28, 420, 200000, 0.0002, 10)
    k1, M1 = get_moment_curvature(400, [507, 126, 126, 507], [80, 225, 375, 520], 28, 420, 200000, 0.0002, 20)
    plt.plot(k, M, "o-")
    plt.plot(k1, M1, "o-")
    plt.show()