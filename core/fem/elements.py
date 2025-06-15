from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import scipy as scipy
import numpy as np
import core.structural_sections as structural_sections
import math as math 
from numpy.typing import NDArray
from typing import Literal, ClassVar

node_index = -1
def set_index() -> int:
    global node_index
    node_index += 1
    return node_index

@dataclass(frozen=True)
class Node: 
    coordinates: tuple[float, float, float]

@dataclass
class FEMElement(ABC):
    nodes: tuple[Node, ...]

    def __post_init__(self)-> None: 
        pass

    @property
    @abstractmethod
    def stiffness_matrix(self) -> NDArray[np.float64]: 
        pass

    @property
    @abstractmethod
    def alt_stiffness_matrix(self) -> NDArray[np.float64]: 
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
    def alt_stiffness_matrix(self) -> NDArray[np.float64]: 
        #DOF 1, 7

        AE: float = self.ReinforcedSection.Section.area * self.ReinforcedSection.elastic_modulus 
        L: float = self.length

        K_comp = AE/L * np.array([
            [1, -1], 
            [-1, 1]
        ], dtype=np.float64)

        EI2: float = self.ReinforcedSection.elastic_modulus * self.ReinforcedSection.Section.get_inertia(local_axis=2)

        K_bending_axis_2 = EI2/L**3 * np.array([
            [12,    6*L,    -12,    6*L],
            [6*L,   4*L**2, -6*L,   2*L**2],
            [-12,   -6*L,   12,     -6*L],
            [6*L,   2*L**2, -6*L,   4*L**2]
        ], dtype=np.float64)
        
        EI3: float = self.ReinforcedSection.elastic_modulus * self.ReinforcedSection.Section.get_inertia(local_axis=3)
        K_bending_axis_3 = EI3/L**3 * np.array([
            [12,    6*L,    -12,    6*L],
            [6*L,   4*L**2, -6*L,   2*L**2],
            [-12,   -6*L,   12,     -6*L],
            [6*L,   2*L**2, -6*L,   4*L**2]
        ], dtype=np.float64)

        J = (self.ReinforcedSection.Section.get_inertia(local_axis=2) 
             + self.ReinforcedSection.Section.get_inertia(local_axis=3)
             )
        GJ = self.ReinforcedSection.Concrete.shear_modulus * J

        K_torsion= GJ/L * np.array([
            [1, -1], 
            [-1, 1]
        ], dtype=np.float64)

        K = np.zeros([12,12])

        K[np.ix_([0,6],[0,6])] = K_comp
        K[np.ix_([1,5,7,11],[1,5,7,11])] = K_bending_axis_2
        K[np.ix_([2,4,8,10],[2,4,8,10])] = K_bending_axis_3
        K[np.ix_([3,9],[3,9])] = K_torsion


        return K

    @property
    def length(self)-> float: 
          ux: float = self.nodes[1].coordinates[0] - self.nodes[0].coordinates[0]
          uy: float = self.nodes[1].coordinates[1] - self.nodes[0].coordinates[1]

          return math.sqrt(ux**2 + uy**2)