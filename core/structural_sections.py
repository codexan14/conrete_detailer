from core.materials import Concrete, Steel
from typing import Literal, Self
from dataclasses import dataclass, field
import math
import core.analysis as analysis

def distance(initial_point: tuple[float, float], final_point: tuple[float,float]) -> float: 
     ux: float = final_point[0] - initial_point[0]
     uy: float = final_point[1] - initial_point[1]

     return math.sqrt(ux**2 + uy**2)

@dataclass
class Section: 
     

@dataclass
class RCRectangularBeamSection: 
     Concrete: Concrete 
     Steel: Steel
     width: float 
     height: float 
     flexural_top_steel_area: float
     flexural_bottom_steel_area: float 
     shear_steel_area: float 
     shear_steel_separation: float 
     cover: float = 40
     flexural_top_steel_edge_to_bar_centroid_distance: float = 40 + 12.7 + 12.7
     flexural_bottom_steel_edge_to_bar_centroid_distance: float = 40 + 12.7 + 12.7

     def get_nominal_moment(self, axis: Literal[1, 2, 3] = 2, sign: Literal['positive', 'negative'] = 'positive') -> float: 
          nominal_moment: float = 0
          if axis == 2 and sign == 'positive':
               nominal_moment = analysis.get_nominal_moment(
                    fc=self.Concrete.compression_strength, 
                    fy = self.Steel.tension_strength,
                    beta_1=self.Concrete.beta_1,
                    b=self.width, 
                    As_top=self.flexural_top_steel_area, 
                    d_top=self.flexural_top_steel_edge_to_bar_centroid_distance,
                    As_bottom=self.flexural_bottom_steel_area,
                    d_bottom=self.height - self.flexural_bottom_steel_edge_to_bar_centroid_distance
               )
          
          elif axis == 2 and sign == 'negative': 
               nominal_moment = - analysis.get_nominal_moment(
                    fc=self.Concrete.compression_strength, 
                    fy = self.Steel.tension_strength,
                    beta_1=self.Concrete.beta_1,
                    b=self.width, 
                    As_top=self.flexural_bottom_steel_area, 
                    d_top=self.flexural_bottom_steel_edge_to_bar_centroid_distance,
                    As_bottom=self.flexural_top_steel_area,
                    d_bottom=self.height - self.flexural_top_steel_edge_to_bar_centroid_distance
               )
          
          return nominal_moment