from abc import ABC, abstractmethod 
from dataclasses import dataclass, field 

@dataclass
class Section: 

     @property
     @abstractmethod
     def area(self) -> float
     centroid: float = field(init=False)

     @

@dataclass
class Bar: 
     pass 

@dataclass
class Shell: 
     pass 

@dataclass
class Solid: 
     pass 
