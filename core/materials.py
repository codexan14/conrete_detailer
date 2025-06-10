from dataclasses import dataclass

@dataclass
class Concrete: 
     compression_resistance: float 
     
     def __post_init__(self): 
          self.elastic_modulus: float = 15100*self.compression_resistance**0.5
          self.beta_1: float = self.get_beta_1()
     
     def get_beta_1(self) -> float: 
          if self.compression_resistance <= 28: 
               beta_1 = 0.85 
          elif self.compression_resistance <= 55: 
               beta_1 = 0.85 + (0.85 - 0.65)/(28 - 55) * (self.compression_resistance - 28)
          else: 
               beta_1 = 0.65 
          
          return beta_1

@dataclass
class Steel: 
     yield_stress: float 

     def __post_init__(self) -> None: 
          self.elastic_modulus: float = 200000 #MPa 
          self.yield_strain: float = self.yield_stress / self.elastic_modulus 

     def stress(self, strain: float): 
          if strain <= -self.yield_strain:
               stress = -self.yield_stress
          elif strain <= self.yield_strain: 
               stress = self.elastic_modulus * strain 
          else: 
               stress = self.yield_stress
          
          return stress 
     
     def strain(self, stress: float) -> float: 
          if stress <= -self.yield_stress:
               raise ValueError("The strain funcion is defined at this stress < -fy")
          elif stress <= self.yield_stress: 
               strain: float = stress / self.elastic_modulus
          else: 
               raise ValueError("The strain funcion is defined at this stress > fy")
          
          return strain 