from core.materials import Concrete, Steel
from core.geometry import Section, RectangularSection
from abc import ABC, abstractmethod
from typing import Literal, Self
from dataclasses import dataclass, field
import math
import core.analysis as analysis

@dataclass
class StructuralSection(ABC):
     Concrete: Concrete
     Steel: Steel 
     Section: RectangularSection

     @property
     @abstractmethod
     def elastic_modulus(self) -> float: 
          pass 


     # @abstractmethod
     # def nominal_moment(self, axis: Literal[1, 2, 3] = 2, sign: Literal['positive', 'negative'] = 'positive')
     #      pass 

     
@dataclass
class RCRectangularBeamSection(StructuralSection):
     flexural_top_steel_area: float = 0
     flexural_bottom_steel_area: float  = 0
     shear_steel_area: float  = 0
     shear_steel_separation: float  = 0
     cover: float = 40
     flexural_top_steel_edge_to_bar_centroid_distance: float = 40 + 12.7 + 12.7
     flexural_bottom_steel_edge_to_bar_centroid_distance: float = 40 + 12.7 + 12.7

     @property 
     def elastic_modulus(self)->float: 
          Ec = self.Concrete.elastic_modulus
          Es = self.Steel.elastic_modulus 
          As = self.flexural_top_steel_area + self.flexural_bottom_steel_area 
          Ac = self.Section.area - As 

          return (Ec*Ac + Es*As)/(Ac + As)

     def get_nominal_moment(self, axis: Literal[1, 2, 3] = 2, sign: Literal['positive', 'negative'] = 'positive') -> float: 
          nominal_moment: float = 0
          if axis == 2 and sign == 'positive':
               nominal_moment = analysis.get_nominal_moment(
                    fc=self.Concrete.compression_strength, 
                    fy = self.Steel.tension_strength,
                    beta_1=self.Concrete.beta_1,
                    b=self.Section.width, 
                    As_top=self.flexural_top_steel_area, 
                    d_top=self.flexural_top_steel_edge_to_bar_centroid_distance,
                    As_bottom=self.flexural_bottom_steel_area,
                    d_bottom=self.Section.height - self.flexural_bottom_steel_edge_to_bar_centroid_distance
               )
          
          elif axis == 2 and sign == 'negative': 
               nominal_moment = - analysis.get_nominal_moment(
                    fc=self.Concrete.compression_strength, 
                    fy = self.Steel.tension_strength,
                    beta_1=self.Concrete.beta_1,
                    b=self.Section.width, 
                    As_top=self.flexural_bottom_steel_area, 
                    d_top=self.flexural_bottom_steel_edge_to_bar_centroid_distance,
                    As_bottom=self.flexural_top_steel_area,
                    d_bottom=self.Section.height - self.flexural_top_steel_edge_to_bar_centroid_distance
               )
          
          return nominal_moment