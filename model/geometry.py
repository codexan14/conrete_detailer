from abc import ABC, abstractmethod 
from dataclasses import dataclass, field 
from typing import Literal
import math as math
@dataclass
class Section(ABC):
     
     @property
     @abstractmethod
     def area(self) -> float: 
          pass

     @abstractmethod
     def get_inertia(self, local_axis: Literal[1, 2, 3]) -> float:
          pass 

@dataclass
class RectangularSection(Section): 
     width: float 
     height: float 

     @property
     def area(self) -> float: 
          return self.width * self.height
     
     def get_inertia(self, local_axis: Literal[1, 2, 3]): 
          if local_axis == 2: 
               inertia = self.width * self.height**3 / 12
          elif local_axis == 3: 
               inertia = self.height * self.width**3 / 12
          else:
               raise Exception("Section doesn't have inertia over local axis 1")
          
          return inertia
     
@dataclass
class Bar_2D: 
     list_of_points: tuple[tuple[float, float], tuple[float, float]]

     @property
     def length(self) -> float: 
          ux = self.list_of_points[1][0] - self.list_of_points[0][0]
          uy = self.list_of_points[1][1] - self.list_of_points[0][1]

          return math.sqrt(ux**2 + uy**2)


@dataclass
class Shell: 
     pass 

@dataclass
class Solid: 
     pass 
