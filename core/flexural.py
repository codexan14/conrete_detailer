# ANALYSIS PART
from core.utils import numeric_solver
from core.materials import get_beta_1, get_steel_stress, get_concrete_stress
from typing import Callable

def get_phi(): 
    return 0.90

def flexural_equilibrium_equation(c):
    equilibrium = 0 
    
    concrete_force(theta, c, b)

    for As, d in zip(rebar_areas, rebar_positions):
        equilibrium += As * get_steel_stress((ec/c)*(c - d)) 

    equilibrium += external_force 

    return equilibrium
        



def get_reduced_nominal_moment_beam_no_compression_reinforcement(
        base: float, 
        steel_area: float,
        rebar_centroid: float,
        concrete_compression_strength: float = 28,
        steel_yield_stress: float = 420
) -> float:
    b = base
    d = rebar_centroid # from extreme compression fiber
    fc = concrete_compression_strength
    fy = steel_yield_stress
    As = steel_area
    
    a = As*fy / (0.85*fc * b)
    phi = 0.9
    Mn = As*fy*(d-a/2)
    return phi*Mn

def get_reduced_nominal_moment_beam_with_compression_reinforcement(
        base: float, 
        tension_rebar_area: float,
        tension_rebar_centroid: float,
        compression_rebar_area: float, 
        compression_rebar_centroid: float,
        concrete_compression_strength: float = 28,
        steel_yield_stress: float = 420
) -> float:
    b = base
    d = tension_rebar_centroid # from extreme compression fiber
    As = tension_rebar_area
    fy = steel_yield_stress
    fc = concrete_compression_strength
    dp = compression_rebar_centroid
    Asp = compression_rebar_area

#.  0 = Cc + Cs - Ts
#.  0 = 0.85*fc*a*b + Asp*fsp - As*fs
#.  0 = 0.85*fc*beta_1*b + Asp*stress(strainfsp) - As*stress(strain)
#.  0 = 0.85*fc*beta_1*b + Asp*stress(theta*(c-d)) - As*stress(theta*(dp - c))
#.  0 = 0.85*fc*beta_1*b + Asp*stress((0.003/c)*(c-d)) - As*stress((0.003/c)*(dp - c)) 
    beta_1 = get_beta_1(fc) 

    equilibrium: Callable[[float], float] = lambda c: (
        0.85*fc*beta_1*c*b
        + Asp * get_steel_stress((0.003/c)*(c-dp), fy)
        - As * get_steel_stress((0.003/c) * (d - c), fy)
    )

    c = numeric_solver(equilibrium, 0, 0.001*d, d, 1e-10)


    phi = get_phi() 
    Mn = (
        0.85*fc*beta_1*c*b*(d - beta_1*c/2) 
        + Asp * get_steel_stress((0.003/c)*(c-dp), fy) * (d - dp))
    
    return phi*Mn


#DESIGN PART

if __name__ == '__main__': 
    assert abs(get_reduced_nominal_moment_beam_no_compression_reinforcement(300, 2*507, 540, 28, 420) - 195546559.7647059) < 1e-10
    assert abs(get_reduced_nominal_moment_beam_with_compression_reinforcement(300, 2*507,540, 0, 0, 28, 420) - 195546559.7647059) < 1e-10
