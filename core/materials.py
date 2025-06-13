from dataclasses import dataclass, field
import math 
from abc import ABC, abstractmethod

@dataclass
class LinearElastic(ABC):
     elastic_modulus: float = field(init = False)
     compression_strength: float = field(init=False)
     tension_strength: float = field(init = False) 
     shear_strength: float = field(init = False)
     poison_ration: float = field(init=False)


@dataclass
class Concrete(LinearElastic): 
     compression_strength: float 
     
     def __post_init__(self) -> None: 
          self.elastic_modulus: float = 15100*self.compression_strength**0.5
          self.beta_1: float = self.get_beta_1()
          self.tension_strength: float = 0.56 * math.sqrt(self.compression_strength)

     def get_beta_1(self) -> float: 
          if self.compression_strength <= 28: 
               beta_1 = 0.85 
          elif self.compression_strength <= 55: 
               beta_1 = 0.85 + (0.85 - 0.65)/(28 - 55) * (self.compression_strength - 28)
          else: 
               beta_1 = 0.65 
          
          return beta_1

@dataclass
class Steel(LinearElastic): 
     tension_strength: float 

     def __post_init__(self) -> None: 
          self.compression_strength: float = -self.tension_strength
          self.elastic_modulus: float = 200000 #MPa 
          self.yield_strain: float = self.tension_strength / self.elastic_modulus 

     def stress(self, strain: float): 
          if strain <= -self.yield_strain:
               stress = -self.tension_strength
          elif strain <= self.yield_strain: 
               stress = self.elastic_modulus * strain 
          else: 
               stress = self.tension_strength
          
          return stress 
     
     def strain(self, stress: float) -> float: 
          if stress <= -self.tension_strength:
               raise ValueError("The strain funcion is defined at this stress < -fy")
          elif stress <= self.tension_strength: 
               strain: float = stress / self.elastic_modulus
          else: 
               raise ValueError("The strain funcion is defined at this stress > fy")
          
          return strain 