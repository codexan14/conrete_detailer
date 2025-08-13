from core.beam_flexion_lrfd import get_beam_positive_nominal_moment, get_beam_negative_nominal_moment
from core.beam_torsion_lrfd import get_nominal_torsion_strength

def get_bending_torsion_interaction(
        web_width: float, 
        height: float, 
        concrete_compression_strength: float, 
        longitudinal_reinforcement_yield_stress: float,
        shear_reinforcement_yield_stress: float,
        top_reinforcement_area: float, 
        top_reinforcement_centroid: float,
        bottom_reinforcement_area: float, 
        bottom_reinforcement_centroid: float,
        skin_reinforcement_area: float,
        enclosed_area_by_outter_stirrup: float,
        stirrup_separation: float,
        outter_stirrup_leg_area: float, 
        outter_stirrup_perimeter: float,
        steel_strain_max: float 
) -> None: 

    longitudinal_reinforcement_area: float = (
        top_reinforcement_area + 
        bottom_reinforcement_area + 
        skin_reinforcement_area
    )
    
    Mn: float = get_beam_positive_nominal_moment(
        web_width=web_width, 
        height=height, 
        concrete_compression_strength=concrete_compression_strength, 
        top_reinforcement_area =top_reinforcement_area, 
        top_reinforcement_centroid=top_reinforcement_centroid,
        bottom_reinforcement_area=bottom_reinforcement_area, 
        bottom_reinforcement_centroid=bottom_reinforcement_centroid,
        steel_strain_max=steel_strain_max
    )

    Tn: float = get_nominal_torsion_strength(
        enclosed_area_by_outter_stirrup=enclosed_area_by_outter_stirrup,
        longitudinal_reinforcement_area=longitudinal_reinforcement_area,
        outter_stirrup_leg_area=outter_stirrup_leg_area, 
        longitudinal_reinforcement_yield_stress=longitudinal_reinforcement_yield_stress, 
        shear_reinforcement_yield_stress=shear_reinforcement_yield_stress, 
        stirrup_separation=stirrup_separation,
        outter_stirrup_perimeter=outter_stirrup_perimeter)

def get_shear_torsion_interaction() -> None: 
    pass 

if __name__ == '__main__':
    pass 