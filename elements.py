from typing import Literal
import numpy as np 
import math as math

from dataclasses import dataclass
from materials import Concrete, Steel
from ezdxf.document import Drawing
from ezdxf.layouts.layout import Modelspace

import units 
import ezdxf

MODEL_UNITS: dict[str, str]={
     "LENGTH": "mm",
     "MASS": "kg",
     "FORCE": "N"
     }

@dataclass
class ConcreteSection: 
     width: float 
     height: float 
     Concrete: Concrete 

@dataclass
class Rebar: 
     diameter: float 
     quantity: int 
     Steel: Steel

     def __post_init__(self):
          self.area: float = self.get_area() 

     def get_area(self) -> float: 
          return self.quantity * 1/4 * math.pi * self.diameter**2
     
@dataclass
class Stirrup: 
     diameter: float 
     quantity: int 
     spacing: float
     Steel: Steel

     def __post_init__(self):
          self.area: float = self.get_area() 

     def get_area(self) -> float: 
          return self.quantity * 1/4 * math.pi * self.diameter**2
     
@dataclass
class ReinforcedConcreteBeamSection: 
     ConcreteSection: ConcreteSection 
     TopRebar: Rebar 
     BottomRebar: Rebar 
     Stirrup: Stirrup
     cover: float = 40

     def get_positive_nominal_moment(self): 
          # Cc + Cs + Ts = 0 
          # 0.85*fc*a*b + As_top*fs_top + As_bottom * fs_bottom = 0
          # Asume que el acero superior no fluye. Asume que el acero inferior fluye
          # 0.85*fc*beta_1*c*b + As_top*Es*steel_train_top - As_bottom * fy = 0
          
          # Relacion de triangulos:
          # steel_train_top = steel_train_top/(c-d') * (c-d') = steel_strain_bottom/(c-d) * (c-d')
          #Sustituir
          # 0.85*fc*beta_1*c*b + As_top*Es*steel_strain_bottom * (c-d') - As_bottom * fy = 0
          # 0.85*fc*beta_1*c*b*(c-d) + As_top*Es*steel_strain_bottom * (c-d') - As_bottom * fy * (c-d) = 0
          # 0.85*fc*beta_1*c**2*b - 0.85*fc*beta_1*c*b*d + As_top*Es*steel_strain_bottom * c - As_top*Es*steel_strain_bottom * d' - As_bottom * fy * c - As_bottom * fy * d = 0
          # 0.85*fc*beta_1*c**2*b  + c*(-0.85*fc*beta_1*b*d + As_top*Es*steel_strain_bottom - As_bottom * fy) - (As_top*Es*steel_strain_bottom * d'  - As_bottom * fy * d) = 0
          
          fc: float = self.ConcreteSection.Concrete.compression_resistance
          beta_1: float = self.ConcreteSection.Concrete.beta_1
          b: float = self.ConcreteSection.width 
          d_bottom: float = self.ConcreteSection.height - self.cover
          Es: float = self.BottomRebar.Steel.elastic_modulus
          As_top: float = self.TopRebar.area
          As_bottom: float = self.BottomRebar.area
          d_top: float = self.cover
          steel_bottom_strain = -0.005
          fy: float = self.BottomRebar.Steel.yield_stress

          A:float = 0.85*fc*beta_1*b
          B:float =  -0.85*fc*beta_1*b*d_bottom + As_top*Es*steel_bottom_strain - As_bottom * fy
          C:float = -As_top*Es*steel_bottom_strain * d_top  + As_bottom * fy * d_bottom

          print(A, B, C)                       
          c: float = (-B - (B**2 - 4*A*C)**0.5) / (2*A)
          a: float = beta_1*c
          print(c)
          nominal_moment: float = As_bottom*fy*(d_bottom - d_top) - 0.85*fc*beta_1*c*b*(a/2 - d_top)

          return nominal_moment
     
# @dataclass 
# class Beam: 
#      width: float
#      height: float
#      length: float
#      bottom_continuous_bar_qty: int = 2
#      bottom_non_continuous_bar_qty: int = 0
#      superior_continuous_bar_qty: int = 2 
#      superior_left_additional_bar_qty: int = 2 
#      superior_right_additional_bar_qty: int = 2


#      cover: float = 40
#      bottom_continuous_bar_size: int = 25
#      bottom_non_continuous_bar_size: int = 25
#      superior_continuous_bar_size: int = 25
#      superior_left_additional_bar_size: int = 19 
#      superior_right_additional_bar_size: int = 19
#      stirrup_diameter: int = 10

#      def get_positive_nominal_moment(section: int) -> None: 
#           pass 

#      def get_negative_nominal_moment(section: int) -> None: 
#           pass 

#      def __post_init__(self): 
#           self.stirrup_90_degree_bend_diameter: float = 4 * self.stirrup_diameter
     
#      def __convert_to_SI_units__(self) -> None: 
#           self.width: float =      self.width * units.INPUT_LENGTH_FACTOR[MODEL_UNITS["LENGTH"]]
#           self.height: float =       self.height * units.INPUT_LENGTH_FACTOR[MODEL_UNITS["LENGTH"]]
#           self.cover: float =       self.cover * units.INPUT_LENGTH_FACTOR[MODEL_UNITS["LENGTH"]]
     
#      def __revert_to_user_units_(self) -> None: 
#           self.width: float = self.width / units.INPUT_LENGTH_FACTOR[MODEL_UNITS["LENGTH"]]
#           self.height: float = self.height / units.INPUT_LENGTH_FACTOR[MODEL_UNITS["LENGTH"]]
#           self.cover: float = self.cover / units.INPUT_LENGTH_FACTOR[MODEL_UNITS["LENGTH"]]


#      def plot_section(self, name: str ):
#           name = name
#           self.__revert_to_user_units_()

#           doc: Drawing = ezdxf.new()
#           msp: Modelspace = doc.modelspace()

#           # Concrete Part
#           msp.add_polyline2d(
#                points=[
#                     (0, 0), 
#                     (0, self.height), 
#                     (self.width, self.height),
#                     (self.width, 0)
#                     ], 
#                close=True, 
#                dxfattribs={
#                     "layer": "CONCRETE"
#                })
          
#           # Flex Rebar
#           bottom_bars_spacing: float = (self.width - 2*self.cover - 2*self.stirrup_diameter - self.stirrup_90_degree_bend_diameter + (self.stirrup_90_degree_bend_diameter - self.bottom_continuous_bar_size)*0.707106)/(self.bottom_continuous_bar_qty+self.bottom_non_continuous_bar_qty - 1)

#           bottom_bars_horizontal_position: list[tuple[float, float]] = [self.cover + self.stirrup_diameter + self.stirrup_90_degree_bend_diameter/2 - (self.stirrup_90_degree_bend_diameter - self.bottom_continuous_bar_size)*0.707106/2  + bottom_bars_spacing*i for i in range(self.bottom_continuous_bar_qty+self.bottom_non_continuous_bar_qty)]

#           for x in bottom_bars_horizontal_position: 
#                msp.add_circle(
#                     center=(
#                          x, 
#                          self.cover + self.stirrup_diameter + self.stirrup_90_degree_bend_diameter/2 - (self.stirrup_90_degree_bend_diameter - self.bottom_continuous_bar_size)*0.707106/2), radius=self.bottom_continuous_bar_size/2
#                          )
               
#           # Stirrups Part
#           msp.add_polyline2d(
#                points=[
#                     (self.cover, self.cover), 
#                     (self.cover, self.height - self.cover), 
#                     (self.width - self.cover, self.height - self.cover),
#                     (self.width - self.cover, self.cover)
#                     ], 
#                close=True, 
#                dxfattribs={
#                     "layer": "STIRRUPS"
#                })
          
#           doc.saveas(name)
#           self.__convert_to_SI_units__()