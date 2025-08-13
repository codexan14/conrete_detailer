import math 
from core.beam_shear_lrfd import get_nominal_concrete_section_shear_strength

def get_torsion_reduction_factor() -> float: 
    return 0.75 

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
        min(concrete_compression_strength**0.5, 8.3) * 
        encolsed_area_by_outter_stirrup**2 / 
        cross_section_perimeter * 
        (
            1 + ultimate_axial_load/(
                0.33 * gross_area * Lambda * min(concrete_compression_strength, 8.3)**0.5)
        )**0.5
    )

    return cracking_torsion

def get_nominal_torsion_strength_by_stirrups(
        enclosed_area_by_outter_stirrup: float, # area enclosed by centerline of the outermost closed transverse torsional reinforcement, mm2
        outter_stirrup_leg_area: float, 
        shear_reinforcement_yield_stress: float, 
        stirrup_separation: float,
        ) -> float:  

    theta: float = math.pi / 4
    Ao: float = 0.85 * enclosed_area_by_outter_stirrup   # Ao: gross area enclosed by torsional shear flow path (mm2)
    torsional_Stregnth_by_stirrups: float = 2 * Ao * outter_stirrup_leg_area * shear_reinforcement_yield_stress / (stirrup_separation * math.tan(theta))
    
    return torsional_Stregnth_by_stirrups

def get_nominal_torsion_strength_by_longitudinal_reinforcement(
        enclosed_area_by_outter_stirrup: float, # area enclosed by centerline of the outermost closed transverse torsional reinforcement, mm2
        longitudinal_reinforcement_area: float,
        longitudinal_reinforcement_yield_stress: float, 
        outter_stirrup_perimeter: float
        ) -> float:  

    theta: float = math.pi / 4  # By 22.7.6.1.2 
    Ao: float = 0.85 * enclosed_area_by_outter_stirrup   # Ao: gross area enclosed by torsional shear flow path (mm2)
    torsional_Stregnth_by_stirrups: float = 2 * Ao * longitudinal_reinforcement_area * longitudinal_reinforcement_yield_stress / (outter_stirrup_perimeter * math.tan(theta))
    
    return torsional_Stregnth_by_stirrups

def get_nominal_torsion_strength(
        enclosed_area_by_outter_stirrup: float, # area enclosed by centerline of the outermost closed transverse torsional reinforcement, mm2
        longitudinal_reinforcement_area: float,
        outter_stirrup_leg_area: float, 
        longitudinal_reinforcement_yield_stress: float, 
        shear_reinforcement_yield_stress: float, 
        stirrup_separation: float,
        outter_stirrup_perimeter: float
        ) -> float: 
    
    return min(
        get_nominal_torsion_strength_by_stirrups(
            enclosed_area_by_outter_stirrup=enclosed_area_by_outter_stirrup, # area enclosed by centerline of the outermost closed transverse torsional reinforcement, mm2
            outter_stirrup_leg_area=outter_stirrup_leg_area, 
            shear_reinforcement_yield_stress=shear_reinforcement_yield_stress, 
            stirrup_separation=stirrup_separation),
        get_nominal_torsion_strength_by_longitudinal_reinforcement(
            enclosed_area_by_outter_stirrup=enclosed_area_by_outter_stirrup, # area enclosed by centerline of the outermost closed transverse torsional reinforcement, mm2
            longitudinal_reinforcement_area=longitudinal_reinforcement_area,
            longitudinal_reinforcement_yield_stress=longitudinal_reinforcement_yield_stress, 
            outter_stirrup_perimeter=outter_stirrup_perimeter)
    )

def verify_cross_section_limit(
        web_width: float,
        gross_area: float,
        tension_reinforcement_area: float,
        tension_reinforcement_centroid: float,
        shear_reinforcement_area: float, 
        shear_reinforcement_spacing: float,
        outter_stirrup_perimeter: float,
        enclosed_area_by_outter_stirrup: float, # area enclosed by centerline of the outermost closed transverse torsional reinforcement, mm2
        concrete_compression_strength: float,
        shear_reinforcement_yield_stress: float,
        ultimate_axial_load: float,
        ultimate_shear: float,
        ultimate_torsion: float
) -> bool: 
    
    phi: float = get_torsion_reduction_factor()

    capacity: float = (
        (ultimate_shear/ (web_width*tension_reinforcement_centroid))**2 + 
        (ultimate_torsion * outter_stirrup_perimeter/(1.7 * enclosed_area_by_outter_stirrup**2))**2
    )**0.5

    nominal_concrete_shear_strength: float = get_nominal_concrete_section_shear_strength(
        web_width=web_width,
        gross_area=gross_area,
        tension_reinforcement_area=tension_reinforcement_area,
        tension_reinforcement_centroid=tension_reinforcement_centroid, # measured from most compressed fiber
        shear_reinforcement_area=shear_reinforcement_area, 
        shear_reinforcement_spacing=shear_reinforcement_spacing,
        concrete_compression_strength=concrete_compression_strength, 
        shear_reinforcement_yield_stress=shear_reinforcement_yield_stress, 
        ultimate_axial_load=ultimate_axial_load)
    
    limit: float = (
        phi*(nominal_concrete_shear_strength / (web_width*tension_reinforcement_centroid) + 
        0.66 * min(concrete_compression_strength**0.5, 8.3)))
    
    return capacity < limit

if __name__ == '__main__':
    pass