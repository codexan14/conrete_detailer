
def shear_reduction_factor() -> float: 
    return 0.60

def get_minimum_shear_reinforcement_area(
        web_width: float, 
        concrete_compression_strength: float,
        shear_reinforcement_yield_stress: float, 
        shear_reinforcement_spacing: float, 

) -> float: # ACI 318-19 - Table 9.6.3.4
    return 0.062 * max(concrete_compression_strength, 31.8678)**0.5 * web_width * shear_reinforcement_spacing / shear_reinforcement_yield_stress

def get_nominal_concrete_section_shear_strength(
        web_width: float,
        gross_area: float,
        tension_reinforcement_area: float,
        tension_reinforcement_centroid: float, # measured from most compressed fiber
        shear_reinforcement_area: float, 
        shear_reinforcement_spacing: float,
        concrete_compression_strength: float, 
        shear_reinforcement_yield_stress: float, 
        axial_load: float) -> float: 

    minimum_shear_reinforcement_area: float = get_minimum_shear_reinforcement_area(
        web_width=web_width, 
        concrete_compression_strength=concrete_compression_strength, 
        shear_reinforcement_yield_stress=shear_reinforcement_yield_stress,
        shear_reinforcement_spacing=shear_reinforcement_spacing)
    
    Lambda: float = 1 # No lightweight concrete yet.

    if shear_reinforcement_area > minimum_shear_reinforcement_area: 
        concrete_section_shear_strength: float = (
            0.17 * (concrete_compression_strength)**0.5 + 
            axial_load / (6 * gross_area)
        ) * web_width * tension_reinforcement_centroid

    else: 
        
        Lambda_s: float = min(1, (2/(1 + 0.004 * tension_reinforcement_centroid)) ** 0.5)    # size factor
        rho_w: float = tension_reinforcement_area / (web_width * tension_reinforcement_centroid)

        concrete_section_shear_strength: float = (
            0.66 * Lambda_s * Lambda * (rho_w)**(1/3) * (concrete_compression_strength)**0.5 + axial_load/(6*gross_area)
        ) * web_width * tension_reinforcement_centroid

    concrete_section_shear_strength_limit: float = 0.42 * Lambda * (concrete_compression_strength) ** 0.5 * web_width * tension_reinforcement_centroid

    return min(concrete_section_shear_strength, concrete_section_shear_strength_limit)


def get_nominal_shear_reinforcement_strength(
        shear_reinforcement_area: float,
        tension_reinforcement_centroid: float,
        shear_reinforcement_spacing: float,
        shear_reinforcement_yield_stress: float, 
) -> float: 
    
    nominal_shear_reinforcement_strength: float = (
        shear_reinforcement_area * shear_reinforcement_yield_stress * tension_reinforcement_centroid
    ) / shear_reinforcement_spacing
    
    return nominal_shear_reinforcement_strength

def ultimate_shear_force_limit(
        web_width: float,
        gross_area: float,
        tension_reinforcement_area: float,        
        tension_reinforcement_centroid: float, 
        shear_reinforcement_area: float,
        shear_reinforcement_spacing: float, 
        concrete_compression_strength: float,
        shear_reinforcement_yield_stress: float,
        axial_load: float)-> float:   
    
    phi: float = shear_reduction_factor() 
    Vc: float = get_nominal_concrete_section_shear_strength(
        web_width=web_width, 
        gross_area=gross_area, 
        tension_reinforcement_area=tension_reinforcement_area, 
        tension_reinforcement_centroid=tension_reinforcement_centroid, 
        shear_reinforcement_area=shear_reinforcement_area, 
        shear_reinforcement_spacing=shear_reinforcement_spacing, 
        concrete_compression_strength=concrete_compression_strength, 
        shear_reinforcement_yield_stress=shear_reinforcement_yield_stress, 
        axial_load=axial_load)

    # ACI 318-19: 22.5.1.2
    return phi*(Vc + 0.66 * concrete_compression_strength**0.5 * web_width * tension_reinforcement_centroid)

def get_nominal_section_shear_strength(
        web_width: float, 
        gross_area: float,
        tension_reinforcement_area: float, 
        tension_reinforcement_centroid: float,
        shear_reinforcement_area: float, 
        shear_reinforcement_spacing: float,
        concrete_compression_strength: float, 
        shear_reinforcement_yield_stress: float,
        axial_load: float) -> float: 
    
    nominal_concrete_section_shear_strength: float = get_nominal_concrete_section_shear_strength(
        web_width=web_width, 
        gross_area=gross_area, 
        tension_reinforcement_area=tension_reinforcement_area, 
        tension_reinforcement_centroid=tension_reinforcement_centroid, 
        shear_reinforcement_area=shear_reinforcement_area, 
        shear_reinforcement_spacing=shear_reinforcement_spacing, 
        concrete_compression_strength=concrete_compression_strength, 
        shear_reinforcement_yield_stress=shear_reinforcement_yield_stress, 
        axial_load=axial_load)
    
    nominal_shear_reinforcement_strength: float = get_nominal_shear_reinforcement_strength(
        shear_reinforcement_area=shear_reinforcement_area,
        shear_reinforcement_yield_stress=shear_reinforcement_yield_stress, 
        tension_reinforcement_centroid=tension_reinforcement_centroid,
        shear_reinforcement_spacing=shear_reinforcement_spacing)

    return nominal_concrete_section_shear_strength + nominal_shear_reinforcement_strength

if __name__ == '__main__':
    pass 
    