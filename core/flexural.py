# ANALYSIS PART
from core.utils import numeric_solver
from core.materials import get_beta_1, get_steel_stress, get_concrete_stress
from typing import Callable

## ULTIMATE LOAD ANALYSIS
def nominal_force_concrete_contribution(fc: float, c: float, b: float) -> float: 
    concrete_force = 0.85*fc*get_beta_1(fc)*c*b 

    return concrete_force

def nominal_moment_concrete_contribution(fc: float, c: float, b: float, pivot_point: float) -> float: 
    concrete_force = nominal_force_concrete_contribution(fc, c, b) 
    leg = pivot_point - get_beta_1(fc) * c / 2 

    return concrete_force * leg 

def nominal_force_steel_contribution(rebar_areas: list[float], rebar_positions: list[float], fy: float, c: float) -> float: 
    steel_force = 0 
    for area, position in zip(rebar_areas, rebar_positions): 
        theta = 0.003 / c
        strain = theta*(c - position)
        stress = get_steel_stress(strain, fy)
        steel_force += stress * area
    
    return steel_force

def nominal_moment_steel_contribution(rebar_areas: list[float], rebar_positions: list[float], fy: float, c: float, pivot_point: float) -> float:
    steel_moment = 0 
    for area, position in zip(rebar_areas, rebar_positions): 
        theta = 0.003 / c
        strain = theta*(c - position)
        stress = get_steel_stress(strain, fy)
        steel_force = stress * area
        leg = pivot_point - position
        steel_moment += steel_force * leg 
    
    return steel_moment

def get_equilibrium_at_nominal_capacity(fc: float, c: float, b: float, rebar_areas: list[float], rebar_positions: list[float], fy: float, P: float = 0) -> float:
    concrete_force: float = nominal_force_concrete_contribution(fc, c, b)
    steel_force: float = nominal_force_steel_contribution(rebar_areas, rebar_positions, fy, c)

    equilibrium = concrete_force + steel_force - P 

    return equilibrium

def get_neutral_axis_at_nominal_capacity(fc: float, b: float, rebar_areas: list[float], rebar_positions: list[float], fy: float, P: float = 0) -> float: 
    equilibrium_function: Callable[[float], float] = lambda c: get_equilibrium_at_nominal_capacity(fc, c, b, rebar_areas, rebar_positions, fy, P) 

    neutral_axis = numeric_solver(equilibrium_function, goal = 0, x1 = 0.01*max(rebar_positions), x2 = max(rebar_positions), error = 1e-20)

    return neutral_axis

def get_reduced_nominal_beam_moment(
        fc: float, 
        b: float, 
        rebar_areas: list[float], 
        rebar_positions: list[float], 
        fy: float, 
        P: float = 0, 
        pivot_point: float = 0,
): 
    c = get_neutral_axis_at_nominal_capacity(fc, b, rebar_areas, rebar_positions, fy, P)

    concrete_nominal_moment: float = nominal_moment_concrete_contribution(fc, c, b, pivot_point=0)
    steel_nominal_moment: float = nominal_moment_steel_contribution(rebar_areas, rebar_positions, fy, c, pivot_point=0)

    moment = concrete_nominal_moment + steel_nominal_moment 

    phi = get_phi()

    return phi*moment


## ELASTIC ANALYSIS
def elastic_concrete_force(fc: float, theta: float, c: float, b: float)-> float: 
    concrete_force = 0 
    for i in range(1, 11): 
        strain = theta*c*i/10
        concrete_force += get_concrete_stress(strain, fc, 'Hognestad') * b * c / 10
    
    return concrete_force

def elastic_concrete_moment(fc: float, theta: float, c: float, b: float, pivot_point: float = 0)-> float: 
    concrete_moment = 0

    for i in range(1, 11): 
        strain = theta*c*i/10
        concrete_force = get_concrete_stress(strain, fc, 'Hognestad') * b * c / 10
        concrete_moment += concrete_force * (pivot_point - c*i/10)

    return concrete_moment

def elastic_steel_force(rebar_areas: list[float], rebar_positions: list[float], theta: float, c: float, fy: float): 
    steel_force: float = 0
    for area, position in zip(rebar_areas, rebar_positions): 
        strain = theta * (c - position)
        stress = get_steel_stress(strain, fy)
        steel_force += stress * area 
    
    return steel_force


def elastic_steel_moment(rebar_areas: list[float], rebar_positions: list[float], theta: float, c: float, fy: float, pivot_point: float): 
    steel_moment: float = 0
    for area, position in zip(rebar_areas, rebar_positions): 
        strain = theta * (c - position)
        stress = get_steel_stress(strain, fy)
        steel_force = stress * area 
        leg = pivot_point - position
        steel_moment += steel_force * leg
    
    return steel_moment

def elastic_moment()
    
def get_equilibrium_at_elastic_condition(
        fc: float, 
        theta: float,
        b: float,
        c: float,
        rebar_areas: list[float], 
        rebar_positions: list[float], 
        fy: float,
        P: float = 0
): 
    
    concrete_force = elastic_concrete_force(fc, theta, c, b)
    steel_force = elastic_steel_force(rebar_areas, rebar_positions, theta, c, fy)

    return concrete_force + steel_force - P

def get_neutral_axis_at_elastic_condition(
        fc: float, 
        theta: float, 
        b: float, 
        rebar_areas: list[float],
        rebar_positions: list[float], 
        fy: float 
) -> float: 
    
    equilibrium: Callable[[float], float] = lambda c: get_equilibrium_at_elastic_condition(fc, theta, b, c, rebar_areas, rebar_positions, fy, 0 )

    neutral_axis: float = numeric_solver(equilibrium, 0, 0.01 * max(rebar_positions), max(rebar_positions), 1e-10)

    return neutral_axis

def moment_curvature(): 
    MAX_CURVATURE: float = 0.003 / max(rebar_positions) * 2

    for i in range(11): 
        curvature: float = MAX_CURVATURE * i / 10 
        c: float = get_neutral_axis_at_elastic_condition(fc, theta, b, rebar_areas, rebar_positions, fy)
        nominal_moment = moment
    pass 
        

def get_phi(): 
    return 0.90



#DESIGN PART

if __name__ == '__main__': 
    assert abs(get_neutral_axis_at_nominal_capacity(28, 300, [2*507], [560], 420, 0) - 2*507*420 / (0.85 * 28 * 300) / 0.85) <= 1e-5
    print(get_reduced_nominal_beam_moment(28, 300, [507*2], [540], 420, 0, 0))
    