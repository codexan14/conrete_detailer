from typing import Literal

MAX_CONCRETE_DEFORMATION = 0.003 
STEEL_YIELD_STRESS = 0.0021 


# GENERAL FUNCTIONS
def get_stress_linear_elastic(strain: float, elastic_modulus: float) -> float:
    return strain * elastic_modulus

def get_stress_linear_plastic(strain: float, elastic_modulus: float, max_stress: float) -> float: 
    stress: float = get_stress_linear_elastic(strain, elastic_modulus)
    return max(-max_stress, min(stress, max_stress))


## CONCRETE MATERIAL 
def get_concrete_elastic_modulus(fc: float) -> float: 
    return 4700 * (fc)**0.5

def get_concrete_rupture_modulus(fc: float) -> float: 
    return 0.62 * (fc)**0.5

def get_concrete_stress(strain: float, fc: float, method: Literal["Linear", "Hognestad"]="Linear") -> float: 
    stress: float = 0
    if method == "Linear": 
        Ec: float = get_concrete_elastic_modulus(fc)
        stress: float = get_stress_linear_elastic(strain, Ec)
    
    elif method == "Hognestad":
        if strain <= MAX_CONCRETE_DEFORMATION: 
            stress = fc*(2*strain/MAX_CONCRETE_DEFORMATION - (strain/MAX_CONCRETE_DEFORMATION)**2)
    
    if stress > fc:     # FAILURE OF THE STRESS
        stress = 0 
        
    return stress

## STEEL MATERIAL
def get_steel_elastic_modulus(fy: float) -> float: 
    return 200000