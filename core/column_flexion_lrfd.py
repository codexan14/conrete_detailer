
from typing import Callable
import math 
from core.concrete_lrfd import get_beta_1, get_concrete_section_strength
import matplotlib.pyplot as plt 

web_width = 300
height = 600 
corner_reinforcement_bar_area = 507 
middle_reinforcement_bar_area = 285 
middle_reinforcement_bar_number_along_width = 5
middle_reinforcement_bar_number_along_height = 6
outter_stirrup_leg_area = 126
cover = 40
fc = 28
Es = 200_000
# DATOS DEPENDIENTES
corner_reinforcement_bar_diameter = (4 * corner_reinforcement_bar_area / math.pi)**0.5 
outter_stirrup_diameter = (4 * outter_stirrup_leg_area / math.pi)**0.5 
reinforcement_range_along_width = web_width - 2*cover - 2*outter_stirrup_diameter - corner_reinforcement_bar_diameter
reinforcement_range_along_height = height - 2*cover - 2*outter_stirrup_diameter - corner_reinforcement_bar_diameter

reinforcement_separation_along_width = reinforcement_range_along_width / (middle_reinforcement_bar_number_along_width + 1)
reinforcement_separation_along_height = reinforcement_range_along_height / (middle_reinforcement_bar_number_along_height + 1)

corner_reinforcement_centroid: list[tuple[float, float]] = [
    (cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2, cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2), 
    (cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2 + reinforcement_range_along_width, cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2), 
    (cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2 + reinforcement_range_along_width, cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2 + reinforcement_range_along_height), 
    (cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2, cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2 + reinforcement_range_along_height), 
]
corner_reinforcement_areas: list[float] = [corner_reinforcement_bar_area] * 4

middle_reinforcement_along_width_centroid = (
    [(cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2 + reinforcement_separation_along_width + reinforcement_separation_along_width*i, cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2) for i in range(middle_reinforcement_bar_number_along_width)] + 
    [(cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2 + reinforcement_separation_along_width + reinforcement_separation_along_width*i, height - cover - outter_stirrup_diameter - corner_reinforcement_bar_diameter/2) for i in range(middle_reinforcement_bar_number_along_width)]
    )
middle_reinforcement_along_width_areas = [middle_reinforcement_bar_area] * 2 * middle_reinforcement_bar_number_along_width


middle_reinforcement_along_height_centroid = (
    [(cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2, cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2 + reinforcement_separation_along_height*(i+1)) for i in range(middle_reinforcement_bar_number_along_height)] + 
    [(web_width - cover - outter_stirrup_diameter - corner_reinforcement_bar_diameter/2, cover + outter_stirrup_diameter + corner_reinforcement_bar_diameter/2 + reinforcement_separation_along_height*(i+1)) for i in range(middle_reinforcement_bar_number_along_height)]
    )
middle_reinforcement_along_height_areas = [middle_reinforcement_bar_area] * 2 * middle_reinforcement_bar_number_along_height

reinforcement_centroid = corner_reinforcement_centroid + middle_reinforcement_along_width_centroid + middle_reinforcement_along_height_centroid
reinforcement_areas: list[float] = corner_reinforcement_areas + middle_reinforcement_along_width_areas + middle_reinforcement_along_height_areas

print(reinforcement_areas)
ec = 0
es: float = -0.0021 

number_of_points = 20

M = [0] * number_of_points
P = [0] * number_of_points

number_of_points_in_tension = int(number_of_points/2)
for i in range(number_of_points_in_tension): 
    ec: float = -0.0021 + (0.003 + 0.0021)/(number_of_points_in_tension - 1) * i
    es = -0.0021 
    d = height - cover - outter_stirrup_diameter - corner_reinforcement_bar_diameter/2

    if ec == es: 
        c = c = -1e10
    else:   
        c = d/(ec - es) * ec


    Cc = 0.85 * fc * max(0, min(0.85*c, height)) * web_width 
    strain_s = map(lambda x: ec/c * (c-x[1]), reinforcement_centroid)
    stress_s = map(lambda x: Es*max(-0.0021, min(0.0021, x)), strain_s)
    forces_s= list(map(lambda x: x[0]*x[1], zip(reinforcement_areas, stress_s)))
    moments_s = map(lambda x: x[0]*(height/2 - x[1][1]), zip(reinforcement_areas, reinforcement_centroid))
    
    M[i] = Cc*(height/2 -  max(0,min(0.85*c, height))/2) + sum(list(moments_s))
    P[i] = Cc + sum(forces_s)

number_of_points_in_compression = number_of_points - number_of_points_in_tension

for i in range(number_of_points_in_compression): 
    ec = 0.003
    es = -0.0021 + (0.003 + 0.0021)/(number_of_points_in_compression - 1) * i
    d = height - cover - outter_stirrup_diameter - corner_reinforcement_bar_diameter/2
    if ec == es: 
        c = 0
    else:   
        c = d/(ec - es) * ec

    Cc = 0.85 * fc * max(0, min(0.85*c, height)) * web_width
    strain_s = map(lambda x: ec/c * (c-x[1]), reinforcement_centroid)
    stress_s = map(lambda x: Es*max(-0.0021, min(0.0021, x)), strain_s)
    forces_s= list(map(lambda x: x[0]*x[1], zip(reinforcement_areas, stress_s)))
    moments_s = list(map(lambda x: x[0]*(height/2 - x[1][1]), zip(reinforcement_areas, reinforcement_centroid)))
    
    M[number_of_points_in_tension + i] = Cc*(height/2 - max(0,min(0.85*c, height))/2) + sum(moments_s)
    P[number_of_points_in_tension + i] = Cc + sum(forces_s)
    
plt.plot(M, P, 'bo-')
plt.xlabel("M")
plt.ylabel("P")

plt.show()