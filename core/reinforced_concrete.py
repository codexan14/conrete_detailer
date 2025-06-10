from typing import Literal
import numpy as np 
import math as math

from dataclasses import dataclass
from core.materials import Concrete, Steel
from ezdxf.document import Drawing
from ezdxf.layouts.layout import Modelspace

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
     
     def __post_init__(self): 
          self.top_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.TopRebar.diameter/2
          self.bottom_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.BottomRebar.diameter/2

     def get_positive_nominal_moment(self): 
          fc: float = self.ConcreteSection.Concrete.compression_resistance
          beta_1: float = self.ConcreteSection.Concrete.beta_1
          b: float = self.ConcreteSection.width 
          d_bottom: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge
          As_top: float = self.TopRebar.area
          As_bottom: float = self.BottomRebar.area
          d_top: float = self.top_rebar_position_from_edge
          fy: float = self.BottomRebar.Steel.yield_stress
          

          # Cc + Cs + Ts = 0 
          # <- Compresion (-)      -> Tension (+)
          # -0.85*fc*a*b + As_top*fs_top + As_bottom * fs_bottom = 0
          # Asume que el acero superior no fluye. Asume que el acero inferior fluye
          # -0.85*fc*beta_1*c*b + As_top*Es*steel_strain_top + As_bottom * fy = 0
          
          # Deformation Compatibility
          # steel_strain_top = steel_strain_top/(d'-c) * (d'-c) = steel_strain_bottom/(d-c) * (d'-c)

          #Substitution
          # -0.85*fc*beta_1*c*b + As_top*Es*steel_strain_bottom/(d-c) * (d'-c) + As_bottom * fy = 0
          # -0.85*fc*beta_1*c*b*(d-c) + As_top*Es*steel_strain_bottom * (d'-c) + As_bottom * fy * (d-c)= 0
          # -0.85*fc*beta_1*c*b*(d) + 0.85*fc*beta_1*c^2*b + As_top*Es*steel_strain_bottom * (d') - As_top*Es*steel_strain_bottom * (c) + As_bottom * fy * (d) - As_bottom * fy * (c)= 0
          # 0.85*fc*beta_1*c^2*b - c*(0.85*fc*beta_1*b*d + As_top*Es*steel_strain_bottom + As_bottom * fy) + (As_top*Es*steel_strain_bottom * d'  + As_bottom * fy * d) = 0
          # 0.85*fc*beta_1*b*c^2 - (0.85*fc*beta_1*b*d + As_top*Es*steel_strain_bottom + As_bottom * fy)*c + (As_top*Es*steel_strain_bottom * d'  + As_bottom * fy * d) = 0
          # b*c^2 - (b*d + (As_top*Es*steel_strain_bottom + As_bottom * fy)/(0.85*fc*beta_1))*c + (As_top*Es*steel_strain_bottom * d'  + As_bottom * fy * d)/(0.85*fc*beta1) = 0
          
          # steel_strain_bottom = 0.0021, Es*0.0021 = fy
          # b*c^2 - (b*d + (As_top*fy + As_bottom * fy)/(0.85*fc*beta_1))*c + (As_top*fy* d'  + As_bottom * fy * d)/(0.85*fc*beta1) = 0
          # b*c^2 - (b*d + fy*(As_top + As_bottom)/(0.85*fc*beta_1))*c + fy*(As_top*d'  + As_bottom * d)/(0.85*fc*beta1) = 0

          # The term fy/0.85*beta_1*fc can be thought as a ratio of stresses, Rf
          # b*c^2 - (b*d + Rf*(As_top + As_bottom))*c + Rf*(As_top*d'  + As_bottom * d) = 0
          
          #Divide by b
          # c^2 - (d + Rf/b*(As_top + As_bottom))*c + Rf/b*(As_top*d'  + As_bottom * d) = 0

          # Solve the quadratic equation. Ac**2 + B*c + C = 0 
          Rf:float = fy/(0.85*fc*beta_1)
          A:float = 1
          B:float =  - (d_bottom + Rf*(As_top + As_bottom)/b)
          C:float = Rf*(As_top*d_top  + As_bottom* d_bottom)/b

          c: float = (-B - (B**2 - 4*A*C)**0.5) / (2*A)
          a: float = beta_1*c

          nominal_moment: float = As_bottom*fy*(d_bottom - d_top) - 0.85*fc*beta_1*c*b*(a/2 - d_top)

          return nominal_moment
     
     def get_negative_nominal_moment(self) -> float:
          fc: float = self.ConcreteSection.Concrete.compression_resistance
          beta_1: float = self.ConcreteSection.Concrete.beta_1
          b: float = self.ConcreteSection.width 
          d_bottom: float = self.bottom_rebar_position_from_edge
          As_top: float = self.TopRebar.area
          As_bottom: float = self.BottomRebar.area
          d_top: float = self.ConcreteSection.height - self.top_rebar_position_from_edge
          fy: float = self.BottomRebar.Steel.yield_stress

          
          Rf:float = fy/(0.85*fc*beta_1)
          A:float = 1
          B:float =  - (d_top + Rf*(As_top+ As_bottom)/b)
          C:float = Rf*(As_top*d_top  + As_bottom* d_bottom)/b
          
          c: float = (-B - (B**2 - 4*A*C)**0.5)/(2)
          a: float = beta_1*c
          nominal_moment: float = As_top*fy*(d_bottom - d_top) - 0.85*fc*beta_1*c*b*(d_bottom - a/2)

          return nominal_moment
     
     def get_minimum_shear_reinforcement(self) -> float: #Av_min/s
          fc: float = self.ConcreteSection.Concrete.compression_resistance 
          b: float = self.ConcreteSection.width
          fyt: float = self.Stirrup.Steel.yield_stress

          minimum_steel_reinforcement: float =max(0.062*math.sqrt(fc), 0.35)*b/fyt # mm^2 / mm

          return minimum_steel_reinforcement

     def get_nominal_concrete_shear_strength_for_positive_moment(self) -> float: 
          Av_min: float = self.get_minimum_shear_reinforcement()
          Av: float = self.Stirrup.area/self.Stirrup.spacing 
          d_bottom: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge
          fc: float = self.ConcreteSection.Concrete.compression_resistance
          b: float = self.ConcreteSection.width
          As_bottom = self.BottomRebar.area 
          
          # Lambda_ calculation 
          lambda_ = 1.00 #NOT LIGHTWEIGHT CONCRETE 
          lambda_s = min(1, math.sqrt(2/(1+0.004*d_bottom)))

          # Comparison
          if Av >= Av_min: 
               nominal_concrete_shear_strength: float = 0.17*lambda_*math.sqrt(fc)*b*d_bottom
          else: 
               nominal_concrete_shear_strength: float = 0.66*lambda_s*lambda_*(As_bottom/(b*d_bottom))**(1/3) * math.sqrt(fc)*b*d_bottom

          return nominal_concrete_shear_strength
     
     def get_nominal_concrete_shear_strength_for_negative_moment(self) -> float: 
          Av_min: float = self.get_minimum_shear_reinforcement()
          Av: float = self.Stirrup.area/self.Stirrup.spacing 
          d_top: float = self.ConcreteSection.height - self.top_rebar_position_from_edge
          fc: float = self.ConcreteSection.Concrete.compression_resistance
          b: float = self.ConcreteSection.width
          As_top: float = self.TopRebar.area 

          # Lambda_ calculation 
          lambda_ = 1.00 #NOT LIGHTWEIGHT CONCRETE 
          lambda_s = min(1, math.sqrt(2/(1+0.004*d_top)))

          # Comparison
          if Av >= Av_min: 
               nominal_concrete_shear_strength: float = 0.17*lambda_*math.sqrt(fc)*b*d_top
     
          else: 
               nominal_concrete_shear_strength: float = 0.66*lambda_s*lambda_*(As_top/(b*d_top))**(1/3) * math.sqrt(fc)*b*d_top

          return nominal_concrete_shear_strength

     def get_nominal_stirrups_shear_strength_for_positive_moment(self) -> float: 
          Av: float = self.Stirrup.area
          d_bottom: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge
          fyt: float = self.Stirrup.Steel.yield_stress 
          s: float = self.Stirrup.spacing

          return Av*fyt*d_bottom/s
     
     def get_nominal_stirrups_shear_strength_for_negative_moment(self) -> float: 
          Av: float = self.Stirrup.area
          d_top: float = self.ConcreteSection.height - self.top_rebar_position_from_edge
          fyt: float = self.Stirrup.Steel.yield_stress 
          s: float = self.Stirrup.spacing

          return Av*fyt*d_top/s
     
     def get_ultimate_shear_limit_for_positive_moment(self) -> float: 
          phi:float = 0.60 #Shear

          fc: float = self.ConcreteSection.Concrete.compression_resistance 
          b: float = self.ConcreteSection.width 
          d_bottom: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge

          Vc: float = self.get_nominal_concrete_shear_strength_for_positive_moment()

          return phi*(Vc + 0.66*math.sqrt(fc)*b*d_bottom)

     def get_ultimate_shear_limit_for_negative_moment(self) -> float: 
          phi:float = 0.60 #Shear

          fc: float = self.ConcreteSection.Concrete.compression_resistance 
          b: float = self.ConcreteSection.width 
          d_top: float = self.ConcreteSection.height - self.top_rebar_position_from_edge

          Vc: float = self.get_nominal_concrete_shear_strength_for_negative_moment()

          return phi*(Vc + 0.66*math.sqrt(fc)*b*d_top)
     
     def get_nominal_shear_strength_for_positive_moment(self): 
          Vc: float = self.get_nominal_concrete_shear_strength_for_positive_moment()
          Vs: float = self.get_nominal_stirrups_shear_strength_for_positive_moment() 

          return Vc + Vs

     def get_nominal_shear_strength_for_negative_moment(self): 
          Vc: float = self.get_nominal_concrete_shear_strength_for_negative_moment()
          Vs: float = self.get_nominal_stirrups_shear_strength_for_negative_moment() 
          
          return Vc + Vs
     

@dataclass 
class ReinforcedConcreteColumnSection: 
     ConcreteSection: ConcreteSection 
     CornerRebar: Rebar 
     HorizontalRebar: Rebar 
     VerticalRebar: Rebar
     Stirrup: Stirrup
     cover: float = 40



     def __post_init__(self): 
          self.top_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.HorizontalRebar.diameter/2
          self.bottom_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.HorizontalRebar.diameter/2
          self.left_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.VerticalRebar.diameter/2
          self.right_rebar_position_from_edge: float = self.cover + self.Stirrup.diameter + self.VerticalRebar.diameter/2

          self.horizontal_bar_spacing_from_center:float = (self.ConcreteSection.width 
               - self.left_rebar_position_from_edge
               - self.right_rebar_position_from_edge) / (self.HorizontalRebar.quantity/2 + 1)
           
          ---------------++-+/self.horizontal_bar_free_spacing:float = (
               self.horizontal_bar_spacing_from_center - self.HorizontalRebar.diameter)
          

          self.horizontal_rebar_coordinates: list[float] = [0.]


     def interaction_diagram(self, N:int = 10): 
          d: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge
          top_strain: float = -0.003
          print(self.horizontal_rebar_coordinates)
          # for i in range(N): 
          #      bottom_strain: float = -0.003 + (0.0021 + 0.003)/(9)*N

          #      c: float = top_strain * d / (top_strain - bottom_strain)
          #      a=self.ConcreteSection.Concrete.beta_1 * c 


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