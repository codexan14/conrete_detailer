def torsion_reduction_factor() -> float: 
    return 0.60

def get_threshold_torsion(
        concrete_compression_strength: float,
        gross_area: float,
        encolsed_area_by_outter_stirrup: float, 
        cross_section_perimeter: float,
        ultimate_axial_load: float
) -> float:

    Lambda: float = 1.0 # No lightweight concrete.

    # ACI 318-19: Table 22.7.4.1: Tth = 0.083 λ sqrt{fc} (Acp**2/pcp) * sqrt{1 + Nu/(0.33 Ag λ sqrt{fc} )}
    threshold_torsion: float = (
        0.083 * Lambda*
        min(concrete_compression_strength, 8.3)**0.5 * 
        encolsed_area_by_outter_stirrup**2 / 
        cross_section_perimeter * 
        (
            1 + ultimate_axial_load/(
                0.33 * gross_area * Lambda * min(concrete_compression_strength, 8.3)**0.5)
        )**0.5
    )

    return threshold_torsion


def get_cracking_torsion(
        concrete_compression_strength: float,
        gross_area: float,
        encolsed_area_by_outter_stirrup: float, 
        cross_section_perimeter: float,
        ultimate_axial_load: float
) -> float:

    Lambda: float = 1.0 # No lightweight concrete.

    # ACI 318-19: Table 22.7.4.1: Tth = 0.083 λ sqrt{fc} (Acp**2/pcp) * sqrt{1 + Nu/(0.33 Ag λ sqrt{fc} )}
    cracking_torsion: float = (
        0.33 * Lambda*
        min(concrete_compression_strength, 8.3)**0.5 * 
        encolsed_area_by_outter_stirrup**2 / 
        cross_section_perimeter * 
        (
            1 + ultimate_axial_load/(
                0.33 * gross_area * Lambda * min(concrete_compression_strength, 8.3)**0.5)
        )**0.5
    )

    return cracking_torsion





if __name__ == '__main__':
    pass 
    