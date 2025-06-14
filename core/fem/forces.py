from dataclasses import dataclass
from core.fem.elements import Node, B2D2
from abc import ABC, abstractmethod
from typing import Literal
from numpy.typing import NDArray
import numpy as np 

@dataclass
class Load(ABC):
    load_case: str

    @property
    @abstractmethod 
    def equivalent_FEM_force(self) -> dict[B2D2, list[NDArray[np.float64]]]:
        # for each element provided (first list), it returns a list (second list) of 
        # vecotr forces [NDArray] for each node of the element
        # list of elements
        #   element 1
        #       node 1
        #           force_vector
        #       node 2 
        #       node 3
        #   element 2
        #   element 3
        pass 

@dataclass
class PunctualForceOnBeams(Load): 
    magnitud: float 
    axis: tuple[Literal[1,2,3], Literal['global', 'local']]
    position: float
    elements: list[B2D2]

    @property
    def equivalent_FEM_force(self) -> dict[B2D2, list[NDArray[np.float64]]]:
        dict_of_forces: dict[B2D2, list[NDArray[np.float64]]] = {}
        for element in self.elements:
            dict_of_forces[element] = [
                np.array([1,2,3,4,5,6]),
                np.array([7,8,9,10,11,12])
            ]
        
        return dict_of_forces