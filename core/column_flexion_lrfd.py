
from typing import Callable

from core.concrete_lrfd import get_beta_1, get_concrete_section_strength


def get_strain_at_position_given_neutral_axis(
        position: float,
        neutral_axis: float,
        known_strain: float, 
        position_of_known_strain: float) -> float: 
    
    strain: float = known_strain/(position_of_known_strain - neutral_axis) * (position - neutral_axis)
    
    return strain

def get_nominal_bending_moment_nominal_force(
        web_width: float, 
        height: float, 
        corner_bar_reinforcement_area: float, 
        middle_bar_reinforcement_area: float,
         
        concrete_compression_strength: float,
        number_of_points: int
) -> tuple[list[float], list[float]]: 
    
    nominal_bending_moment_list: list[float] = [0] * number_of_points
    nominal_axial_force_list: list[float] = [0] * number_of_points

    # P = 0.85*fc*a*b
    # P = 0.85*fc*beta_1*c*b 
    # P = 0.85*fc*beta_1*max(c,h) * b 
    concrete_force: Callable[[float], float] = lambda c: get_concrete_section_strength(
        web_width=web_width, 
        height=height, 
        concrete_compression_strength=concrete_compression_strength, 
        neutral_axis_distance=c
    )

    steel_force: 
    # Steel
    # S = As_i * fs_i 
    # S = As_i * get_stress_given (es_i)
    # S = As_i * get_stress_given (get_strain(centroid_i, c, 0.003, 0)) 
    # S = 


    return nominal_bending_moment_list, nominal_axial_force_list