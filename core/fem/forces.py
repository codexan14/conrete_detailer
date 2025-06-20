from dataclasses import dataclass, field
from core.fem.elements import Node, B2D2, FEMElement
from abc import ABC, abstractmethod
from typing import Literal
from numpy.typing import NDArray
import numpy as np 

@dataclass
class Load(ABC): 
    load_case: str
    nodes: list[Node] = field(init = False)
    forces: list[NDArray[np.float64]] = field(init = False)
    
@dataclass
class PunctualForceBeam(Load): 
    magnitud: float 
    local_axis: Literal[1,2,3]
    element: B2D2
    relative_position: float #position from node 1 in local axis 1

    def __post_init__(self) -> None: 
        self.nodes = [node for node in self.element.nodes]
        self.forces = self.generate_forces()

    def generate_forces(self) -> list[NDArray[np.float64]]: 
        ar: float = self.relative_position
        L: float = self.element.length
        br: float = 1- ar
        P: float = self.magnitud 

        
        if self.local_axis == 1: 
            forces: list[NDArray[np.float64]] = [
                np.array([P*ar, 0, 0, 0, 0, 0], dtype=np.float64), 
                np.array([P*br, 0, 0, 0, 0, 0], dtype=np.float64)
            ]
        elif self.local_axis == 2: 
            forces: list[NDArray[np.float64]] = [
                np.array([0, P * br**2 * (2*ar +1), 0, 0, 0, P * br**2 * ar * L], dtype=np.float64), 
                np.array([0, P * ar**2 * (3 -2*ar), 0, 0, 0, P * ar**2 * (-br) * L], dtype=np.float64)
            ]
        else: 
            forces: list[NDArray[np.float64]] = [
                np.array([0, 0, P * br**2 * (2*ar +1), 0, P * br**2 * ar * L, 0] , dtype=np.float64), 
                np.array([0, 0, P * ar**2 * (3 -2*ar), 0, P * ar**2 * (-br) * L, 0], dtype=np.float64)
            ]

        return forces