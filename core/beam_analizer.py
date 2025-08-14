from core.beam_flexion_lrfd import get_beam_positive_nominal_moment, get_beam_negative_nominal_moment
from core.beam_torsion_lrfd import get_nominal_torsion_strength, get_threshold_torsion, get_cracking_torsion
import matplotlib.pyplot as plt

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
        steel_strain_max: float, 
        number_of_points: int
) -> tuple[list[float], list[float]]: 

    nominal_torsion_list: list[float] = [0] * number_of_points 
    nominal_moment_list: list[float] = [0] * number_of_points
    
    for point in range(0, number_of_points): 
        x: float = point / (number_of_points)     # Parameter for redistributing the steel: 

        top_longitudinal_reinforcement_area_in_torsion: float = top_reinforcement_area * x
        bottom_longitudinal_reinforcement_area_in_torsion: float = bottom_reinforcement_area * x

        top_reinforcement_area_in_flexion: float = top_reinforcement_area - top_longitudinal_reinforcement_area_in_torsion
        bottom_reinforcement_area_in_flexion: float = bottom_reinforcement_area - bottom_longitudinal_reinforcement_area_in_torsion

        longitudinal_reinforcement_area_in_torsion: float = (
            skin_reinforcement_area + 
            top_longitudinal_reinforcement_area_in_torsion + 
            bottom_longitudinal_reinforcement_area_in_torsion)

        Mn: float = get_beam_positive_nominal_moment(
            web_width=web_width, 
            height=height, 
            concrete_compression_strength=concrete_compression_strength, 
            top_reinforcement_area =top_reinforcement_area_in_flexion, 
            top_reinforcement_centroid=top_reinforcement_centroid,
            bottom_reinforcement_area=bottom_reinforcement_area_in_flexion, 
            bottom_reinforcement_centroid=bottom_reinforcement_centroid,
            steel_strain_max=steel_strain_max
        )

        Tn: float = get_nominal_torsion_strength(
            enclosed_area_by_outter_stirrup=enclosed_area_by_outter_stirrup,
            longitudinal_reinforcement_area=longitudinal_reinforcement_area_in_torsion,
            outter_stirrup_leg_area=outter_stirrup_leg_area, 
            longitudinal_reinforcement_yield_stress=longitudinal_reinforcement_yield_stress, 
            shear_reinforcement_yield_stress=shear_reinforcement_yield_stress, 
            stirrup_separation=stirrup_separation,
            outter_stirrup_perimeter=outter_stirrup_perimeter)
        
        nominal_torsion_list[point] = Tn 
        nominal_moment_list[point] = Mn 
        
    return nominal_moment_list, nominal_torsion_list

def get_reduced_bending_torsion_interaction(
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
        steel_strain_max: float, 
        ultimate_axial_load: float,
        number_of_points: int
) -> tuple[list[float], list[float], list[float]]: 
    
    nominal_moment_list: list[float]
    nominal_torsion_list: list[float]

    nominal_moment_list, nominal_torsion_list= get_bending_torsion_interaction(
        web_width=web_width, 
        height=height, 
        concrete_compression_strength=concrete_compression_strength, 
        longitudinal_reinforcement_yield_stress=longitudinal_reinforcement_yield_stress,
        shear_reinforcement_yield_stress=shear_reinforcement_yield_stress,
        top_reinforcement_area=top_reinforcement_area, 
        top_reinforcement_centroid=top_reinforcement_centroid,
        bottom_reinforcement_area=bottom_reinforcement_area, 
        bottom_reinforcement_centroid=bottom_reinforcement_centroid,
        skin_reinforcement_area=skin_reinforcement_area,
        enclosed_area_by_outter_stirrup=enclosed_area_by_outter_stirrup,
        stirrup_separation=stirrup_separation,
        outter_stirrup_leg_area=outter_stirrup_leg_area, 
        outter_stirrup_perimeter=outter_stirrup_perimeter,
        steel_strain_max=steel_strain_max, 
        number_of_points=number_of_points
)

    threshold_torsion: float = get_threshold_torsion(
        concrete_compression_strength=concrete_compression_strength,
        gross_area=web_width*height,
        encolsed_area_by_outter_stirrup=enclosed_area_by_outter_stirrup, 
        cross_section_perimeter=outter_stirrup_perimeter,
        ultimate_axial_load=ultimate_axial_load
    )

    cracking_torsion: float = get_cracking_torsion(
        concrete_compression_strength=concrete_compression_strength,
        gross_area=web_width*height,
        encolsed_area_by_outter_stirrup=enclosed_area_by_outter_stirrup, 
        cross_section_perimeter=outter_stirrup_perimeter,
        ultimate_axial_load=ultimate_axial_load
    )

    reduced_nominal_bending_list: list[float] = [0] * number_of_points
    reduced_nominal_torsion_list: list[float] = [0] * number_of_points
    reduced_redistributed_nominal_torsion_list: list[float] = [0] * number_of_points

    for point in range(number_of_points): 

        if nominal_torsion_list[point] <= threshold_torsion: 
            reduced_nominal_bending_list[point] = 0.90 * max(nominal_moment_list)  # Ignores torsion if below threshold
            reduced_nominal_torsion_list[point] = 0.65 * nominal_torsion_list[point]
            reduced_redistributed_nominal_torsion_list[point] = 0.65 * nominal_torsion_list[point]
        elif nominal_torsion_list[point] <= cracking_torsion: 
            reduced_nominal_bending_list[point] = 0.90 * nominal_moment_list[point]  # Ignores torsion if below threshold
            reduced_nominal_torsion_list[point] = 0.65 * nominal_torsion_list[point]
            reduced_redistributed_nominal_torsion_list[point] = 0.65 * nominal_torsion_list[point]
        else: 
            reduced_nominal_bending_list[point] = 0.90 * nominal_moment_list[point]  # Ignores torsion if below threshold
            reduced_nominal_torsion_list[point] = 0.65 * nominal_torsion_list[point]
            reduced_redistributed_nominal_torsion_list[point] = 0.65 * cracking_torsion

    return reduced_nominal_bending_list, reduced_nominal_torsion_list, reduced_redistributed_nominal_torsion_list

def get_shear_torsion_interaction() -> None: 
    pass 

if __name__ == '__main__':
    moment_and_torsion: tuple[list[float], list[float]]= get_bending_torsion_interaction(
        web_width=600, 
        height=1000, 
        concrete_compression_strength=28, 
        longitudinal_reinforcement_yield_stress=420,
        shear_reinforcement_yield_stress=420,
        top_reinforcement_area=4*507, 
        top_reinforcement_centroid=70,
        bottom_reinforcement_area=4*507, 
        bottom_reinforcement_centroid=930,
        skin_reinforcement_area=6*285,
        enclosed_area_by_outter_stirrup=(600-80)*(1000-80),
        stirrup_separation=100,
        outter_stirrup_leg_area=126, 
        outter_stirrup_perimeter=2*(1000+600),
        steel_strain_max=0.0021, 
        number_of_points=100)
    
    reduced_moment_and_torsion: tuple[list[float], list[float], list[float]]= get_reduced_bending_torsion_interaction(
        web_width=600, 
        height=1000, 
        concrete_compression_strength=28, 
        longitudinal_reinforcement_yield_stress=420,
        shear_reinforcement_yield_stress=420,
        top_reinforcement_area=4*507, 
        top_reinforcement_centroid=70,
        bottom_reinforcement_area=4*507, 
        bottom_reinforcement_centroid=930,
        skin_reinforcement_area=6*285,
        enclosed_area_by_outter_stirrup=(600-80)*(1000-80),
        stirrup_separation=100,
        outter_stirrup_leg_area=126, 
        outter_stirrup_perimeter=2*(1000+600),
        steel_strain_max=0.0021, 
        ultimate_axial_load=0,
        number_of_points=100)
    
    
    plt.plot(moment_and_torsion[0], moment_and_torsion[1], 'b--')
    plt.plot(reduced_moment_and_torsion[0], reduced_moment_and_torsion[1], 'r--')
    plt.plot(reduced_moment_and_torsion[0], reduced_moment_and_torsion[2], 'y--')
    cracking_torsion: float = get_cracking_torsion(
        concrete_compression_strength=28,
        gross_area=300*600, 
        encolsed_area_by_outter_stirrup=220*520, 
        cross_section_perimeter=1480,
        ultimate_axial_load=0
    )
    plt.xlabel("Moment")
    plt.ylabel("Torsion")
    plt.show()
