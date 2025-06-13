from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import scipy as scipy
import numpy as np
import core.structural_sections as structural_sections
import math as math 
from numpy.typing import NDArray
from typing import Literal

element_index = 0
node_index = 0

@dataclass
class Node: 
    index: int = field(init=False)
    coordinates: tuple[float, float, float]

    def __post_init__(self) -> None: 
        global node_index 
        self.index = node_index 
        node_index += 1

@dataclass
class FEMElement(ABC):
    index: int
    nodes: tuple[Node, ...]

    def __post_init__(self)-> None: 
        global element_index 
        self.index = element_index 
        element_index += 1

    @property
    @abstractmethod
    def stiffness_matrix(self) -> NDArray[np.float64]: 
        pass

    
@dataclass
class B2D2(FEMElement): 
    ReinforcedSection: structural_sections.StructuralSection

    @property
    def stiffness_matrix(self) -> NDArray[np.float64]: 
        AE: float = self.ReinforcedSection.Section.area * self.ReinforcedSection.elastic_modulus 
        EI: float = self.ReinforcedSection.elastic_modulus * self.ReinforcedSection.Section.get_inertia(local_axis=2)
        L: float = self.length

        return np.array(
            [
                [AE/L,  0,              0,          -AE/L,  0,              0], 
                [0,     12*EI/L**3,     6*EI/L**2,  0,      -12*EI/L**3,    6*EI/L**2],
                [0,     6*EI/L**2,      4*EI/L,     0,      -6*EI/L**2,     2*EI/L],
                [-AE/L, 0,              0,          AE/L,   0,              0],
                [0,     -12*EI/L**3,    -6*EI/L**2, 0,      12*EI/L**3,     -6*EI/L**2],
                [0,     6*EI/L**2,      2*EI/L,     0,      -6*EI/L**2,     4*EI/L],
            ], dtype=np.float64
        )
    
    @property
    def length(self)-> float: 
          ux: float = self.nodes[1][0] - self.nodes[0][0]
          uy: float = self.nodes[1][1] - self.nodes[0][1]

          return math.sqrt(ux**2 + uy**2)