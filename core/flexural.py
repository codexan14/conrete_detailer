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