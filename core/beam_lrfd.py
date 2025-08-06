import pandas as pd 
from typing import Callable

CONCRETE_MAX_DEFORMATION = 0.003

def read_beam_sections_csv(path: str) -> pd.DataFrame: 
    beam_sections: pd.DataFrame = pd.read_csv(path, sep=',') #type: ignore
    return beam_sections

def get_beta_1(concrete_strength: float) -> float: 
    # ACI 318: β_1 varies with f'c between 0.65 and 0.85
    return min(0.85, max(0.65, 0.85 - 0.0020*(concrete_strength - 30)))

def concrete_force_capacity(
        concrete_strength: float, 
        base: float, 
        neutral_axis_distance: float) -> float: 
    
    # Concrete force = 0.85*fc*a*b = 0.85*fc*β_1*c*b
    return 0.85*concrete_strength*get_beta_1(concrete_strength=concrete_strength)*neutral_axis_distance*base

def strain_at_position_given_neutral_axis(
        position: float, 
        neutral_axis_distance: float, 
        rebar_position_bottom: float, 
        steel_max_strain: float = 0.0021) -> float: 
    
    # Angle θ due to deformation: θ = ε_smax / (d - c)
    theta: float = steel_max_strain/(rebar_position_bottom - neutral_axis_distance)

    # Strain ε at given position y: ε = θ * (c - y)
    strain: float = theta * (neutral_axis_distance - position)
    
    return strain

def steel_stress(steel_strain: float, steel_yield_stress: float = 420, steel_max_strain: float = 0.0021) -> float: 
    # The steel stress is between -E*ε_smax and E*ε_smax
    return steel_yield_stress * min(1, max(-1, steel_strain/steel_max_strain))

def steel_force_capacity(steel_area: float, steel_strain: float) -> float: 
    # Fs = As * fs
    return steel_area * steel_stress(steel_strain)

def solve(function: Callable[[float], float], target: float, initial_value_1: float, initial_value_2: float, error: float = 0.10) -> float:
    """
    Uses the numerical method called bisection method. Where two initial values x1 and x2 are given
    and the function should return values y1 and y2 with different signs
    """
    x1: float = initial_value_1
    x2: float = initial_value_2

    y1: float = function(x1)
    y2: float = function(x2)

    # Asserts that the two initial values give two outputs with different signs.
    assert int(y2/abs(y2)) != int(y1/abs(y1))

    # First approximation of the solution
    x: float = x1 + (target - y1)*(x2-x1)/(y2-y1)
    

    while abs(function(x) - target) > error: # Iterates until the function is near the target within an error. 
        y: float = function(x)
        if int(y1/abs(y1)) == int(y/abs(y)): # signs are equal
            x1 = x
            y1 = y
        else: 
            x2 = x
            y2 = y

        x: float = x1 + (target - y1)*(x2-x1)/(y2-y1)

    return x

def calculate_beam_maximum_bottom_reinforcement(
        base: float,
        rebar_area_top: float,
        rebar_position_top: float, 
        rebar_position_bottom: float, 
        concrete_strength: float, 
        steel_yield_stress: float,
        steel_young_modulus: float = 200_000,
        max_concrete_strain: float = 0.003, 
        max_steel_strain: float = 0.0021) -> float: 
    
    # beta_1:               typically between 0.65 - 0.85
    beta_1: float = get_beta_1(concrete_strength=concrete_strength)

    # neutral axis:         c = d/(ε_c + ε_s) * ε_c
    c: float = rebar_position_bottom/(max_concrete_strain + max_steel_strain) * max_concrete_strain

    # top rebar stress:     fs' = Es * (ε_c - (ε_c + ε_s)/d * d')
    fst: float = steel_young_modulus * (max_concrete_strain -  (max_concrete_strain + max_steel_strain)/rebar_position_bottom * rebar_position_top)
    
    # bottom rebar stress   fs = fy
    fsb: float = steel_yield_stress

    # maximum bottom rebar area     As = (0.85*fc*β_1*c*b + As' * fs')/fs
    bottom_rebar_area: float = (0.85*concrete_strength*beta_1*c*base + rebar_area_top*fst)/fsb 

    return bottom_rebar_area

def calculate_beam_positive_moment_capacity(
        base: float, 
        height: float, 
        concrete_strength: float,
        rebar_area_top: float, 
        rebar_area_bottom: float, 
        rebar_position_top: float, 
        rebar_position_bottom: float,
        steel_max_strain: float = 0.0021) -> float: 
    
    # See the concrete_force_capacity function: 0.85*fc*a*b
    concrete_force: Callable[[float], float] = lambda c: concrete_force_capacity(
        concrete_strength=concrete_strength, 
        base=base, 
        neutral_axis_distance=c)
    
    top_steel_strain: Callable[[float],float] = lambda c: strain_at_position_given_neutral_axis(
        position = rebar_position_top, 
        neutral_axis_distance = c, 
        rebar_position_bottom = rebar_position_bottom, 
        steel_max_strain = steel_max_strain)
    
    # See the steel_force_capacity function: As*fs
    top_steel_force: Callable[[float], float] = lambda c: steel_force_capacity(
        steel_area=rebar_area_top, 
        steel_strain=top_steel_strain(c))

    # Bottom Steel is assumed to yield
    bottom_steel_strain: float = -0.0021

    # See the steel_force_capacity function: As*fs
    bottom_steel_force: Callable[[float], float] = lambda c: steel_force_capacity(
        steel_area=rebar_area_bottom, 
        steel_strain=bottom_steel_strain)

    # Equilibrium of forces, in terms of c, with lambda functions. Cc + Cs - Ts = 0
    equilibrium: Callable[[float], float] = lambda c: concrete_force(c) + top_steel_force(c) + bottom_steel_force(c)

    # Neutral axis is found by minimizing the function f=Cc+Cs-Ts up to zero. 
    neutral_axis: float = solve(equilibrium, 20, 0, height/2, 0.00001)
    
    beta_1: float = get_beta_1(concrete_strength=concrete_strength)
    
    moment_capacity: float = (
        concrete_force(neutral_axis)*(rebar_position_bottom - beta_1*neutral_axis/2) + 
        top_steel_force(neutral_axis)*(rebar_position_bottom - rebar_position_top))
    
    return moment_capacity

def calculate_beam_negative_moment_capacity(
        base: float, 
        height: float, 
        concrete_strength: float,
        rebar_area_top: float, 
        rebar_area_bottom: float, 
        rebar_position_top: float, 
        rebar_position_bottom: float,
        steel_max_strain: float = 0.0021) -> float: 
    
    # See the concrete_force_capacity function: 0.85*fc*a*b
    concrete_force: Callable[[float], float] = lambda c: concrete_force_capacity(
        concrete_strength=concrete_strength, 
        base=base, 
        neutral_axis_distance=c)
    
    top_steel_strain: float = -0.0021

    # See the steel_force_capacity function: As*fs
    top_steel_force: Callable[[float], float] = lambda c: steel_force_capacity(
        steel_area=rebar_area_top, 
        steel_strain=top_steel_strain)

    # Bottom Steel is assumed to yield
    bottom_steel_strain: Callable[[float], float] = lambda c: strain_at_position_given_neutral_axis(
        position = height - rebar_position_bottom, 
        neutral_axis_distance = c, 
        rebar_position_bottom = height - rebar_position_top, 
        steel_max_strain = steel_max_strain)

    # See the steel_force_capacity function: As*fs
    bottom_steel_force: Callable[[float], float] = lambda c: steel_force_capacity(
        steel_area=rebar_area_bottom, 
        steel_strain=bottom_steel_strain(c))

    # Equilibrium of forces, in terms of c, with lambda functions. Cc + Cs - Ts = 0
    equilibrium: Callable[[float], float] = lambda c: concrete_force(c) + top_steel_force(c) + bottom_steel_force(c)

    # Neutral axis is found by minimizing the function f=Cc+Cs-Ts up to zero. 
    neutral_axis: float = solve(equilibrium, 20, 0, height/2, 0.00001)

    beta_1: float = get_beta_1(concrete_strength=concrete_strength)
    
    moment_capacity: float = (
        concrete_force(neutral_axis)*(rebar_position_bottom - beta_1*neutral_axis/2) + 
        bottom_steel_force(neutral_axis)*(rebar_position_bottom - rebar_position_top))
    
    return moment_capacity

if __name__ == '__main__':

    def evaluate(function: Callable[[float], float], eval_value: float, expected_return_value: float, name: str = '', error: float = 0.01) -> None: 
        if name != '': 
            function.__name__ = name
        try: 
            assert abs(function(eval_value) - expected_return_value)/function(eval_value) < error 
            print(f"{function.__name__}: \033[1;32mCORRECT\033[0m, error: {(abs(function(eval_value) - expected_return_value))/function(eval_value)}")
        except AssertionError: 
            print(f"{function.__name__}: \033[1;31mERROR\033[0m, error: {(abs(function(eval_value) - expected_return_value))/function(eval_value)}")

    read_beam_sections_csv(path = r"core/examples/01/beam_sections.csv")

    evaluate(function=get_beta_1, eval_value=28, expected_return_value=0.85, error=0.01)

    evaluate(
        lambda c: concrete_force_capacity(concrete_strength=28, base=300, neutral_axis_distance=c), 
        eval_value=150, expected_return_value=910_350, 
        name = 'concrete_force_capacity', 
        error=0.01)

    evaluate(lambda c: strain_at_position_given_neutral_axis(
        position = 50, 
        neutral_axis_distance = c, 
        rebar_position_bottom = 530, 
        steel_max_strain = 0.0021), eval_value=150, 
        expected_return_value=0.00055263157894736842105, 
        name='strain_at_position_given_neutral_axis')
    

    evaluate(function=steel_stress, eval_value=0.001, expected_return_value=200, error=0.01)
    evaluate(function=steel_stress, eval_value=0.03, expected_return_value=420, error=0.01)
    evaluate(function=steel_stress, eval_value=-0.03, expected_return_value=-420, error=0.01)
    
    evaluate(
        lambda strain: steel_force_capacity(steel_area=5070, steel_strain=strain), 
        eval_value=0.001, 
        expected_return_value=1_014_000, 
        name = 'steel_force_capacity', 
        error=0.01)
    
    evaluate(
        lambda strain: steel_force_capacity(steel_area=5070, steel_strain=strain), 
        eval_value=0.030, 
        expected_return_value=2_129_400, 
        name = 'steel_force_capacity', error=0.01)
    
    evaluate(
        lambda strain: steel_force_capacity(steel_area=5070, steel_strain=strain), 
        eval_value=-0.030, 
        expected_return_value=-2_129_400, 
        name = 'steel_force_capacity', error=0.01)

    evaluate(
        lambda c: solve(lambda x: 0.20*x**3 - x, target=c, initial_value_1=1, initial_value_2=3, error=10e-10), 
        eval_value=0, 
        expected_return_value=2.236068, 
        name="solve",
        error=0.1)
    
    evaluate(lambda rebar_position_top: calculate_beam_maximum_bottom_reinforcement(
        base=300, 
        rebar_area_top=0,
        rebar_position_bottom=530,
        rebar_position_top=rebar_position_top,
        concrete_strength=28,
        steel_yield_stress=420
    ), eval_value=0, expected_return_value=4_505, name='calculate_beam_maximum_bottom_reinforcement')

    evaluate(lambda rebar_area_bottom: calculate_beam_positive_moment_capacity(
        base=300, 
        height=600, 
        concrete_strength=28, 
        rebar_area_top = 2*507, 
        rebar_area_bottom=rebar_area_bottom, 
        rebar_position_top=70, 
        rebar_position_bottom=530), eval_value=5*507, expected_return_value=492230374.53596, name='calculate_beam_positive_positive_capacity')
    
    evaluate(lambda rebar_area_bottom: calculate_beam_negative_moment_capacity(
        base=300, 
        height=600, 
        concrete_strength=28, 
        rebar_area_top = 2*507, 
        rebar_area_bottom=rebar_area_bottom, 
        rebar_position_top=70, 
        rebar_position_bottom=530), eval_value=5*507, expected_return_value=213012147.62379, name='calculate_beam_positive_negative_capacity')