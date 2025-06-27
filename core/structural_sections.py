from core.materials import Concrete, Steel
from core.geometry import Section, RectangularSection
from abc import ABC, abstractmethod
from typing import Literal, Self
from dataclasses import dataclass, field
import math
import core.analysis as analysis
import numpy as np 
from time import sleep 
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
          Ec: float = self.Concrete.elastic_modulus
          Es: float = self.Steel.elastic_modulus 
          As: float = self.flexural_top_steel_area + self.flexural_bottom_steel_area 
          Ac: float = self.Section.area - As 

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
     

@dataclass
class RectangularColumnSection(StructuralSection): 
     corner_steel_diameter: float = 4
     horizontal_steel_diameter: float = 0
     vertical_steel_diameter: float = 0

     horizontal_steel_quantity: float = 0
     vertical_steel_quantity: float = 0

     cover: float = 40
     flexural_top_steel_edge_to_bar_centroid_distance: float = 40 + 12.7 + 12.7
     flexural_bottom_steel_edge_to_bar_centroid_distance: float = 40 + 12.7 + 12.7

     def __post_init__(self): 
          self.steel_area: float = (
               4 * math.pi * (self.corner_steel_diameter/2)**2 
               + 2*self.horizontal_steel_quantity*math.pi * (self.horizontal_steel_diameter/2)**2 
               + 2*self.vertical_steel_quantity* math.pi * (self.vertical_steel_diameter/2)**2)
          
          self.horizontal_steel_spacing = (self.Section.width - 2*self.cover - self.horizontal_steel_diameter)/(self.horizontal_steel_quantity + 2)
          self.vertical_steel_spacing = (self.Section.height - 2*self.cover - self.vertical_steel_diameter)/(self.vertical_steel_quantity + 2)

          
          self.horizontal_steel_position = np.arange(
               start=self.cover + self.horizontal_steel_diameter/2 + self.horizontal_steel_spacing, 
               stop=self.Section.width - self.cover - self.horizontal_steel_diameter/2, 
               step=(self.Section.width - 2*self.cover - self.horizontal_steel_diameter)/self.horizontal_steel_quantity
          )

          self.vertical_steel_position = np.arange(
               start=self.cover + self.vertical_steel_diameter/2 + self.vertical_steel_spacing, 
               stop=self.Section.height - self.cover - self.vertical_steel_diameter/2, 
               step=(self.Section.height - 2*self.cover - self.vertical_steel_diameter)/self.vertical_steel_quantity
          )

          
     @property 
     def elastic_modulus(self)->float: 
          Ec: float = self.Concrete.elastic_modulus
          Es: float = self.Steel.elastic_modulus 
          As: float = self.steel_area
          Ac: float = self.Section.area - As 

          return (Ec*Ac + Es*As)/(Ac + As)

     def get_nominal_moment(self, axis: Literal[1, 2, 3] = 2, sign: Literal['positive', 'negative'] = 'positive') -> float: 
          
          fc = self.Concrete.compression_strength
          b = self.Section.width
          h = self.Section.height
          d = self.flexural_bottom_steel_edge_to_bar_centroid_distance
          F = 1 
          es = 0.01
          
          factor = 10
          while np.abs(F) > 0.01: 
               c = d / (0.003 - es) * 0.003
               a = self.Concrete.beta_1*c
               theta = 0.003/c 

               Cc = -0.85*fc*a*b 
               steel_postition_relative = self.vertical_steel_position - c 
               steel_strain = steel_postition_relative * theta 
               steel_stress = self.Steel.stress(steel_strain)
               print(steel_stress) 

               steel_forces = steel_stress * 1/4 * math.pi * (self.vertical_steel_diameter ** 2)
               if np.sign(F) == np.sign(np.sum(steel_forces) + Cc): 
                    pass 
               else: 
                    factor = factor/10
                    print(" here")
               F = np.sum(steel_forces) + Cc 
               print(factor)
               print(F)
               es = es + np.sign(F)*0.001*factor


               # sleep(1)
               # print("k")
               print(es)
          
          M = 0.85*fc*a*b*(h/2 - a/2) + np.sum(self.steel_area*(steel_postition_relative + c - h/2))
          return M




def iterate(function, function_goal, initial_value = 0,method = 'biseccion', error = 0.1, max_iteration = 100): 
     yo = function(initial_value)
     xo = initial_value 
     print(xo)
     xf = initial_value*1.10
     yf = function(xf)
     print(xf)
     actual_error = 1
     iteration = 0

     while (actual_error > error or iteration <= 100): 
          x = xo + (function_goal - yo)*(xo-xf)/(yo-yf)
          iteration += 1
          
          yo = yf 
          xo = xf

          xf = x 
          yf = function(x)

          actual_error = abs(yf - function_goal)
          print(x)
     
     return x