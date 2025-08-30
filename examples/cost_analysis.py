def slab_concrete_volume(lx: float, ly: float, slab_height: float) -> float: 
    concrete_volume: float = lx * ly * slab_height

    return concrete_volume

def waffle_slab_concrete_volume(beam_width: float, foam_width: float, topping: float, lx: float, ly: float, slab_height: float) -> float: 
    number_of_foam_blocks_x = int(2 * (lx - 2*slab_height + beam_width)/(foam_width + beam_width)) / 2
    number_of_foam_blocks_y = int(2 * (ly - 2*slab_height + beam_width)/(foam_width + beam_width)) / 2
    foam_volume = (number_of_foam_blocks_x * foam_width) * (number_of_foam_blocks_y * foam_width) * (slab_height - topping)
    concrete_volume = lx * ly * slab_height - foam_volume

    return concrete_volume

def beam_concrete_volume(width: float, height: float, length: float): 
    concrete_volume: float = width * height * length

    return concrete_volume

def column_concrete_volume(width: float, height: float, length: float):
    concrete_volume: float = width * height * length

    return concrete_volume

#################
def beam_steel_weight(rebar: dict[float, float], length):
    for diameter in rebar: 
        rebar[diameter] /4 * pi * diameter**2 * length


def column_steel_weight(steel_area, height):
    return steel_area * height







######## VIGAS 
