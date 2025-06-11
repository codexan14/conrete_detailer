from dataclasses import dataclass, field
import numpy as np 
from numpy.typing import NDArray

element_counter = 0

def counter() -> None: 
     global element_counter
     element_counter: int = element_counter + 1

@dataclass
class Element: 
     dofs: int

     Section: ReinforcedConcreteSection

     points: tuple[tuple[float,...], ...]

     local_joint_index: range = field(init=False)
     global_joint_index: range = field(init=False)

     local_dof_index: range  = field(init=False)
     global_dof_index: range = field(init=False)

     def __post_init__(self) -> None: 
          counter()
          self.local_joint_index = range(len(self.points))
          self.local_dof_index = range(len(self.points)*self.dofs)
     

@dataclass
class Beam(Element): 
     def local_stiffness_matrix(self) -> NDArray[np.float64]:
          AE = self.Section.gross_area * self.Section.ConcreteSection.Concrete.elastic_modulus 
          EI=self.Section.ConcreteSection.Concrete.elastic_modulus * self.Section.ge 
          return np.array([
               [AE/L,    0,             0,             -AE/L,    0,             0],
               [0,       12*EI/L**3,    6*EI/L**2,     0,        -12*EI/L**3,   6*EI/L**2],
               [0,       6*EI/L**2,     4*EI/L,         0,       -6*EI/L**2,    2*EI/L],
               [-AE/L,   0,             0,             AE/L,     0,             0],
               [0,       -12*EI/L**3,   -6*EI/L**2,     0,        12*EI/L**3,   -6*EI/L**2],
               [0,       6*EI/L**2,     2*EI/L,         0,        -6*EI/L**2,    4*EI/L],]
          , dtype=np.float64)


@dataclass
class Model: 
     elements: "yes"

