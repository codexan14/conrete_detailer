def get_beta_1(concrete_compression_strength: float) -> float: 
    # ACI 318: β_1 varies with f'c between 0.65 and 0.85
    return min(0.85, max(0.65, 0.85 - 0.0020*(concrete_compression_strength - 30)))


def get_concrete_section_strength(
        web_width: float, 
        height: float,
        concrete_compression_strength: float, 
        neutral_axis_distance: float) -> float: 
    
    # Concrete force = 0.85*fc*a*b = 0.85*fc*β_1*min(c,h)*b
    return 0.85*concrete_compression_strength*get_beta_1(concrete_compression_strength=concrete_compression_strength)*min(neutral_axis_distance, height)*web_width
