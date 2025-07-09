from dataclasses import dataclass, field
from typing import Self

CONCRETE_PRICE = 100 #USD/M3

@dataclass
class Container: 
    name: str = field(init=False)
    unit_price: float = field(init=False)
    quantity: float = field(init=False)
    unit: str = field(init=False)
    sub_containers: list[Self] =field(init=False)

    def get_total_cost(self) -> float:# -> Any: 
        cost: float = 0 
        for sub_container in self.sub_containers: 
            cost += sub_container.quantity * sub_container.unit_price
        
        return cost 
    
@dataclass 
class Concrete(Container):
    quantity: float

    def __post_init__(self) -> None: 
        self.name: str = "CONCRETE"
        self.unit: str = "m3"
        self.unit_price: float = CONCRETE_PRICE

@dataclass
class Steel(Container): 
    quantity: float

    def __post_init__(self) -> None: 
        self.name: str = "CONCRETE"
        self.unit: str = "m3"
        self.unit_price: float = CONCRETE_PRICE

@dataclass
class Beam(Container):
    width: float 
    height: float
    length: float

    def __post_init__(self) -> None: 
        self.sub_containers: list[Container] = []
        self.sub_containers.append(
            Concrete(quantity=self.width * self.height * self.length),
            Steel()
        )
