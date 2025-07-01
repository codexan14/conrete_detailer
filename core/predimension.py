from typing import Literal

def get_one_direction_slab_width(
        length: float, 
        support_condition: Literal["simple supported", "one end continuous", "two ends continuous", "cantilever"],
        roof: bool = False) -> float: 
    
    if (support_condition == "simple supported") and roof:
        width: float = length / 20 
    else: 
        width: float = length / 14

    if (support_condition == "one end continuous") and roof: 
        width: float = length / 24 
    else:
        width: float = length / 16 
    
    if (support_condition == "two ends continuous") and roof:
        width: float = length / 28 
    else: 
        width: float = length / 19 
    
    if (support_condition == "cantilever") and roof: 
        width: float = length / 10 
    else: 
        width: float = length / 7

    return width

def get_two_direction_slab_width(horizontal_length: float, vertical_length: float) -> float:
    ln: float = max(horizontal_length, vertical_length)
    beta: float = max(horizontal_length, vertical_length) / min(horizontal_length, vertical_length) 
    width: float = max(horizontal_length, vertical_length) / (30 + 3 * beta)

    if ln > 3000: 
        width = max(120, width)
    
    if ln <= 3000: 
        width = max(100, width)

    return width 

def get_slab_direction(length: float, width: float): 
    pass 

def get_slab_width():
    return 

def get_equivalent_waffle_width(slab_height: float, beam_base: float, separation: float) -> float: 
    slab_inertia: float = (beam_base + separation)*slab_height**3 / 12
    waffle_slab_width: float = (12 * slab_inertia / beam_base)**(1/3)

    return waffle_slab_width


if __name__ == "__main__": 
    assert "3" == "2"
