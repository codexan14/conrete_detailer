from dataclasses import dataclass, field 
import math 
from typing import Literal 


CONCRETE_PRICE = 1200 
STEEL_PRICE = 2000 

STEEL_DENSITY = 20

@dataclass
class Resource: 
    name: str = field(init=False)
    unit: str = field(init=False)
    unit_price: float = field(init=False)

    quantity: float

class Concrete(Resource): 
    def __post_init__(self): 
        self.name = "CONCRETE"
        self.unit = "M3"
        self.unit_price = 1200

@dataclass
class Element:
    Concrete: Resource = field(init=False)
    Steel: Resource = field(init=False)     #diameter, weight
    # formwork_area: float 
    # foam: dict[float, float]        #size, volume
    # wire_mesh: dict[float, float]   #size, weight

    pass 

@dataclass 
class LongitudinalRebar: 
    diameter: float 
    quantity: float
    length: float
    start_hook_degree: Literal[90, 180, 0]
    end_hook_degree: float

    def hook_length(self, hook_degree: Literal[90, 180, 0]): 
        hook_length: float = 0
        if hook_degree == 90: 
            hook_length = 12*self.diameter - 3*self.diameter + math.pi * 6 * self.diameter / 4
        elif hook_degree == 180: 
            hook_length = 4*self.diameter - 3*self.diameter + math.pi * 6 * self.diameter / 2
        else:
            hook_length = 0
            
    
    def bar_length(self, beam_length, ): 
        return beam_length - 2




@dataclass
class Beam(Element): 
    width: float 
    height: float 
    length: float 
    concrete_resistance: float 

    # STEEL 
    TopRebar: LongitudinalRebar
    BotttomRebar: LongitudinalRebar
    SkinRebar: LongitudinalRebar

    AdditionalTopRebarStart: LongitudinalRebar
    AdditionalTopRebarEnd: LongitudinalRebar
    AdditionalTBottomRebar: LongitudinalRebar

    def __post_init__(self): 
        self._Concrete = Concrete(resistance=self.concrete_resistance, volume=self.width * self.height * self.length)
        
        # for steel in [self.TopRebar, self.BotttomRebar, self.SkinRebar]: 
        #     self.