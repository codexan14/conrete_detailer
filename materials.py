from dataclasses import dataclass

@dataclass
class Concrete: 
     compression_resistance: float 
     
     def __post_init__(self): 
          self.elastic_modulus: float = 15100*self.compression_resistance**0.5 