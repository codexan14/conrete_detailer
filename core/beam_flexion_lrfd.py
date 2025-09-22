from typing import Callable
from core.utils import solve

from core.concrete_lrfd import get_beta_1, get_concrete_section_strength

def get_strain_at_position_given_neural_axis(
        position: float, 
        neutral_axis_distance: float, 
        tension_reinforcement_centroid: float, # Measured from most compressed fiber
        steel_strain_max: float = 0.0021) -> float: 
    
    # Angle θ due to deformation: θ = ε_smax / (d - c)
    theta: float = steel_strain_max/(tension_reinforcement_centroid - neutral_axis_distance)

    # Strain ε at given position y: ε = θ * (c - y)
    strain: float = theta * (neutral_axis_distance - position)
    
    return strain

def get_steel_stress(steel_strain: float, longitudinal_reinforcement_yield_stress: float = 420, steel_strain_max: float = 0.0021) -> float: 
    # The steel stress is between -E*ε_smax and E*ε_smax
    return longitudinal_reinforcement_yield_stress * min(1, max(-1, steel_strain/steel_strain_max))

def get_reinforcement_strength(steel_area: float, steel_strain: float) -> float: 
    # Fs = As * fs
    return steel_area * get_steel_stress(steel_strain)

def get_maximum_tensile_reinforcement(
        web_width: float,
        compression_reinforcement_area: float,
        compression_reinforcement_centroid: float,  # Measured from most compressed fiber
        tension_reinforcement_centroid: float, 
        concrete_compression_strength: float, 
        longitudinal_reinforcement_yield_stress: float,
        steel_young_modulus: float = 200_000,
        concrete_strain_max: float = 0.003, 
        steel_strain_max: float = 0.0021) -> float: 
    
    # beta_1:               typically between 0.65 - 0.85
    beta_1: float = get_beta_1(concrete_compression_strength=concrete_compression_strength)

    # Angle θ due to strain (ε_c + ε_s)/d
    theta: float = (concrete_strain_max + steel_strain_max) / tension_reinforcement_centroid
    
    # neutral axis:         c = d/(ε_c + ε_s) * ε_c = ε_c / θ
    c: float = concrete_strain_max / theta

    # compression reinforcement stress:     fs' = Es * (ε_c - theta * d')
    fsp: float = steel_young_modulus * (concrete_strain_max -  theta * compression_reinforcement_centroid)
    
    # bottom rebar stress   fs = fy
    fs: float = longitudinal_reinforcement_yield_stress

    # maximum bottom rebar area     As = (0.85*fc*β_1*c*b + As' * fs')/fs
    bottom_rebar_area: float = (0.85*concrete_compression_strength*beta_1*c*web_width + compression_reinforcement_area*fsp)/fs 

    return bottom_rebar_area

def get_beam_nominal_moment(
        web_width: float, 
        height: float, 
        concrete_compression_strength: float,
        compression_reinforcement_area: float, 
        compression_reinforcement_centroid: float, 
        tension_reinforcement_area: float, 
        tension_reinforcement_centroid: float,
        steel_strain_max: float = 0.0021) -> float: 
    
    # See the get_concrete_section_strength function: 0.85*fc*a*b
    concrete_force: Callable[[float], float] = lambda c: get_concrete_section_strength(
        web_width=web_width, 
        height=height, 
        concrete_compression_strength=concrete_compression_strength, 
        neutral_axis_distance=c)
    
    compression_reinforcement_strain: Callable[[float],float] = lambda c: get_strain_at_position_given_neural_axis(
        position = compression_reinforcement_centroid, 
        neutral_axis_distance = c, 
        tension_reinforcement_centroid = tension_reinforcement_centroid, 
        steel_strain_max = steel_strain_max)
    
    # See the get_reinforcement_strength function: As*fs
    compression_reinforcement_strength: Callable[[float], float] = lambda c: get_reinforcement_strength(
        steel_area=compression_reinforcement_area, 
        steel_strain=compression_reinforcement_strain(c))

    # Bottom Steel is assumed to yield
    tension_reinforcement_strain: float = -0.0021

    # See the get_reinforcement_strength function: As*fs
    bottom_steel_force: Callable[[float], float] = lambda c: get_reinforcement_strength(
        steel_area=tension_reinforcement_area, 
        steel_strain=tension_reinforcement_strain)

    # Equilibrium of forces, in terms of c, with lambda functions. Cc + Cs - Ts = 0
    equilibrium: Callable[[float], float] = lambda c: concrete_force(c) + compression_reinforcement_strength(c) + bottom_steel_force(c)

    # Neutral axis is found by minimizing the function f=Cc+Cs-Ts up to zero. 
    neutral_axis: float = solve(equilibrium, 20, 0, height/2, 0.001)
    
    beta_1: float = get_beta_1(concrete_compression_strength=concrete_compression_strength)
    
    moment_capacity: float = (
        concrete_force(neutral_axis)*(tension_reinforcement_centroid - beta_1*neutral_axis/2) + 
        compression_reinforcement_strength(neutral_axis)*(tension_reinforcement_centroid - compression_reinforcement_centroid))
    
    return moment_capacity

def get_beam_positive_nominal_moment(web_width: float, 
        height: float, 
        concrete_compression_strength: float,
        top_reinforcement_area: float, 
        top_reinforcement_centroid: float, 
        bottom_reinforcement_area: float, 
        bottom_reinforcement_centroid: float,
        steel_strain_max: float) -> float: 
    
    return get_beam_nominal_moment(web_width=web_width, 
        height=height, 
        concrete_compression_strength=concrete_compression_strength,
        compression_reinforcement_area=top_reinforcement_area, 
        compression_reinforcement_centroid=top_reinforcement_centroid, 
        tension_reinforcement_area=bottom_reinforcement_area, 
        tension_reinforcement_centroid=bottom_reinforcement_centroid,
        steel_strain_max=steel_strain_max
    )

def get_beam_negative_nominal_moment(web_width: float, 
        height: float, 
        concrete_compression_strength: float,
        top_reinforcement_area: float, 
        top_reinforcement_centroid: float, 
        bottom_reinforcement_area: float, 
        bottom_reinforcement_centroid: float,
        steel_strain_max: float) -> float: 
    
    return get_beam_nominal_moment(web_width=web_width, 
        height=height, 
        concrete_compression_strength=concrete_compression_strength,
        compression_reinforcement_area=bottom_reinforcement_area, 
        compression_reinforcement_centroid=height-bottom_reinforcement_centroid, 
        tension_reinforcement_area=top_reinforcement_area, 
        tension_reinforcement_centroid=height-top_reinforcement_centroid,
        steel_strain_max=steel_strain_max
    )

if __name__ == '__main__':

    from core.utils import evaluate

    evaluate(function=get_beta_1, eval_value=28, expected_return_value=0.85, error=0.01)

    evaluate(
        lambda c: get_concrete_section_strength(height=600, web_width=300, concrete_compression_strength=28, neutral_axis_distance=c), 
        eval_value=150, expected_return_value=910_350, 
        name = 'get_concrete_section_strength', 
        error=0.01)

    evaluate(lambda c: get_strain_at_position_given_neural_axis(
        position = 50, 
        neutral_axis_distance = c, 
        tension_reinforcement_centroid = 530, 
        steel_strain_max = 0.0021), eval_value=150, 
        expected_return_value=0.00055263157894736842105, 
        name='get_strain_at_position_given_neural_axis')
    

    evaluate(function=get_steel_stress, eval_value=0.001, expected_return_value=200, error=0.01)
    evaluate(function=get_steel_stress, eval_value=0.03, expected_return_value=420, error=0.01)
    evaluate(function=get_steel_stress, eval_value=-0.03, expected_return_value=-420, error=0.01)
    
    evaluate(
        lambda strain: get_reinforcement_strength(steel_area=5070, steel_strain=strain), 
        eval_value=0.001, 
        expected_return_value=1_014_000, 
        name = 'get_reinforcement_strength', 
        error=0.01)
    
    evaluate(
        lambda strain: get_reinforcement_strength(steel_area=5070, steel_strain=strain), 
        eval_value=0.030, 
        expected_return_value=2_129_400, 
        name = 'get_reinforcement_strength', error=0.01)
    
    evaluate(
        lambda strain: get_reinforcement_strength(steel_area=5070, steel_strain=strain), 
        eval_value=-0.030, 
        expected_return_value=-2_129_400, 
        name = 'get_reinforcement_strength', error=0.01)
    
    evaluate(lambda compression_reinforcement_centroid: get_maximum_tensile_reinforcement(
        web_width=300, 
        compression_reinforcement_area=0,
        tension_reinforcement_centroid=530,
        compression_reinforcement_centroid=compression_reinforcement_centroid,
        concrete_compression_strength=28,
        longitudinal_reinforcement_yield_stress=420
    ), eval_value=0, expected_return_value=4_505, name='get_maximum_tensile_reinforcement')

    evaluate(lambda bottom_reinforcement_area: get_beam_positive_nominal_moment(
        web_width=300, 
        height=600, 
        concrete_compression_strength=28, 
        top_reinforcement_area = 2*507, 
        top_reinforcement_centroid=70,
        bottom_reinforcement_area=bottom_reinforcement_area, 
        bottom_reinforcement_centroid=530,
        steel_strain_max=0.0021), eval_value=5*507, expected_return_value=492230374.53596, name='calculate_beam_positive_positive_capacity')
    
    evaluate(lambda bottom_reinforcement_area: get_beam_negative_nominal_moment(
        web_width=300, 
        height=600, 
        concrete_compression_strength=28, 
        top_reinforcement_area = 2*507, 
        top_reinforcement_centroid=70,
        bottom_reinforcement_area=bottom_reinforcement_area, 
        bottom_reinforcement_centroid=530,
        steel_strain_max=0.0021), eval_value=5*507, expected_return_value=213012147.62379, name='calculate_beam_positive_negative_capacity')