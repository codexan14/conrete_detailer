from dataclasses import dataclass
import math 

STEEL_DENSITY = 7850 / (1000)**3        #KG/MM3
CONCRETE_DENSITY = 2800 / (1000)**3     #KG/MM3

STEEL_PRICE = 1200 / (1000)             #USD/KG
CONCRETE_PRICE = 120 / (1000)**3        #USD/MM3

def concrete_volume(b: float, h: float, L: float) -> float: 
    return b * h * L 

def steel_volume(As: float, L: float) -> float: 
    return As * L 

def steel_weight(As: float, L: float) -> float: 
    return STEEL_DENSITY * steel_volume(As, L)


@dataclass
class Rebar: 
    diameter: float 
    length: float 

    def area(self) -> float: 
        return 1/4 * math.pi * (self.diameter)**2
    
    def cos