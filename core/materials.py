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
def get_beta_1(fc: float) -> float: 
    return max(0.65, min(0.85, 0.85 - 0.05*(fc - 28)/7)) 

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


## STEEL MATERIAL FUNCTIONS
STEEL_ELASTIC_MODULUS = 200_000


def get_steel_stress(strain: float, fy: float) -> float: 
    yield_strain = fy/STEEL_ELASTIC_MODULUS
    stress: float

    if strain <= -yield_strain: 
        stress = -fy
    elif strain <= yield_strain: 
        stress = STEEL_ELASTIC_MODULUS * strain 
    else: 
        stress = fy 
    
    return stress