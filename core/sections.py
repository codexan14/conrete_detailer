from typing import Literal
import numpy as np 
import math as math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from core.materials import LinearElastic, Concrete, Steel
# from ezdxf.document import Drawing
# from ezdxf.layouts.layout import Modelspace

# import ezdxf

MODEL_UNITS: dict[str, str]={
     "LENGTH": "mm",
     "MASS": "kg",
     "FORCE": "N"
     }

@dataclass 
class Section: 
     @property
     @abstractmethod
     def area(self) -> float: 
          pass 

     @abstractmethod
     def get_inertia(self, axis: Literal[1, 2, 'polar']) -> float: 
          pass

@dataclass
class RectangularSection(Section): 
     width: float 
     height: float 

     @property
     def area(self) -> float: 
          return self.width * self.height
     
     def get_inertia(self, axis: Literal[1, 2, 'polar']) -> float: 
          if axis == 1: 
               inertia: float = self.width * self.height**3 / 12
          elif axis == 2: 
               inertia: float = self.height * self.width**3 / 12
          elif axis == 'polar': 
               inertia: float = self.width * self.height**3 / 12 + self.height * self.width**3 / 12
          
          return inertia

@dataclass
class CircularSection(Section): 
     diameter: float 

     @property
     def area(self) -> float: 
          return 1/4 * math.pi * (self.diameter)**2
     
     def get_inertia(self, axis: Literal[1, 2, 'polar']) -> float: 
          if axis == 1 or axis == 2: 
               inertia = math.pi * (self.diameter / 2)**4 / 4 
          elif axis == 'polar': 
               inertia = math.pi * (self.diameter / 2)**4 / 2

          return inertia 


@dataclass
class ReinforcedConcreteSection: 
     ConcreteSection: Section 
     gross_area: float = field(init=False) 
     gross_inertia: float = field(init = False)


# @dataclass 
# class ReinforcedConcreteColumnSection(ReinforcedConcreteSection): 
#      CornerRebar: Rebar 
#      HorizontalRebar: Rebar 
#      VerticalRebar: Rebar
#      Stirrup: Stirrup
#      cover: float = 40



#      def __post_init__(self): 
#           self.top_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.HorizontalRebar.diameter/2
#           self.bottom_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.HorizontalRebar.diameter/2
#           self.left_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.VerticalRebar.diameter/2
#           self.right_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.VerticalRebar.diameter/2

#           self.horizontal_bar_spacing_from_center:float = (self.ConcreteSection.width 
#                - self.left_rebar_position_from_edge
#                - self.right_rebar_position_from_edge) / (self.HorizontalRebar.quantity/2 + 1)
           
#           self.horizontal_bar_free_spacing:float = (
#                self.horizontal_bar_spacing_from_center - self.HorizontalRebar.diameter)
          

#           self.horizontal_rebar_coordinates: list[float] = [0.]


#      def interaction_diagram(self, N:int = 10): 
#           d: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge
#           top_strain: float = -0.003
#           print(self.horizontal_rebar_coordinates)
#           # for i in range(N): 
#           #      bottom_strain: float = -0.003 + (0.0021 + 0.003)/(9)*N

#           #      c: float = top_strain * d / (top_strain - bottom_strain)
#           #      a=self.ConcreteSection.Concrete.beta_1 * c 


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