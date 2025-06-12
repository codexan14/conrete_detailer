from core.materials import * 
from core.sections import * 
from typing import Self

@dataclass
class ConcreteSection: 
     Section: RectangularSection
     Concrete: Concrete 

@dataclass
class SteelSection: 
     position: Literal['top', 'bottom', 'left', 'right', 'corner', 'stirrups']
     diameter: float 
     quantity: int 
     coordinates: list[tuple[float, float]] = field(init=False)
     area: float = field(init=False)

     @abstractmethod
     def define_geometry(self, ContainingSection: ConcreteSection, offset: float = 0) -> None: 
          # Populates the coordinates variable
          pass 

@dataclass 
class Stirrups(SteelSection): 
     stirrup_type: Literal["closed", "single-legged"]
     def __post_init__(self) -> None: 
          if self.position != 'stirrups': 
               raise ValueError("Stirrups can't be used as a Flexural Steel")
          else: 
               pass 
          
          self.area = self.quantity * math.pi / 4 * (self.diameter / 2)**2 
     
     def define_geometry(self, ContainingSection: ConcreteSection, offset: float = 0) -> None:
          if self.stirrup_type == "closed":
               self.inner_width: float = ConcreteSection.Section.width - 2*offset - 2*self.diameter
               self.inner_height: float = ConcreteSection.Section.height - 2*offset - 2*self.diameter
          if self.stirrup_type == "single-legged":
               self.inner_width: float = 0
               self.inner_height: float = ConcreteSection.Section.height - 2*offset - 2*self.diameter

               

@dataclass
class FlexuralSteel(SteelSection): 
     def __post_init__(self) -> None: 
          if self.position == 'stirrups': 
               raise ValueError("Flexural Steel can't be used as a stirrups")
          else: 
               pass 
          
          self.area = self.quantity * math.pi / 4 * (self.diameter / 2)**2 

     def define_geometry(self, ContainingSection: ConcreteSection, offset: float = 0) -> None:
          width: float = ContainingSection.Section.width
          height: float = ContainingSection.Section.height
          number_of_bars: int = self.quantity

          if self.position == 'top': 
               y: float = height - offset - self.diameter/2
               self.coordinates: list[tuple[float, float]] = [
                    (offset + (width - 2*offset)/(number_of_bars-1) * i, y) for i in range(number_of_bars)
                    ]
               
          elif self.position == 'bottom': 
               y: float = offset + self.diameter/2
               self.coordinates: list[tuple[float, float]] = [
                    (offset + (width - 2*offset)/(number_of_bars-1) * i, y) for i in range(number_of_bars)
                    ]
          
          elif self.position == 'left': 
               x: float = offset + self.diameter/2
               self.coordinates: list[tuple[float, float]] = [
                    (x, offset + (height - 2*offset)/(number_of_bars-1) * i) for i in range(number_of_bars)
                    ]
          
          elif self.position == 'right': 
               x: float = width - offset - self.diameter/2
               self.coordinates: list[tuple[float, float]] = [
                    (x, offset + (height - 2*offset)/(number_of_bars-1) * i) for i in range(number_of_bars)
                    ]
          elif self.position == 'corner': 
               self.coordinates: list[tuple[float, float]] = [
                    (offset + self.diameter/2, offset + self.diameter/2), 
                    (width - offset - self.diameter/2, offset + self.diameter/2),
                    (width - offset - self.diameter/2, height - offset - self.diameter/2),
                    (offset + self.diameter/2, height - offset - self.diameter/2)
                    ]
          
          else: 
               self.coordinates: list[tuple[float, float]] = [
                    ]

@dataclass
class ReinforcedConcreteSection: 
     ConcreteSection: ConcreteSection 
     flexural_steel_list: list[FlexuralSteel]
     stirrups_list: list[Stirrups]
     cover: float = 40 

     def __post_init__(self) -> None: 
          for stirrup in self.stirrups_list: 
               stirrup.define_geometry(ContainingSection= self.ConcreteSection, offset=self.cover)

          main_stirrup_diameter: float = self.stirrups_list[0].diameter
          for flexural_steel in self.flexural_steel_list: 
               flexural_steel.define_geometry(ContainingSection=self.ConcreteSection, offset=self.cover + main_stirrup_diameter)
          
     def get_flexural_coord_from_edge(self, side: Literal['top', 'bottom', 'left', 'right']) -> float: 
          first_moment_axis_1: float = 0
          first_moment_axis_2: float = 0
          total_area: float = 0

          for Rebar in self.flexural_steel_list: 
               for coords in Rebar.coordinates:
                    if Rebar.position == side: 
                         first_moment_axis_1 += Rebar.area/Rebar.quantity * coords[0]
                         first_moment_axis_2 += Rebar.area/Rebar.quantity * coords[1]
                         total_area += Rebar.area/Rebar.quantity
          
          if side == 'top' or side == 'bottom':
               distance_from_edge: float = first_moment_axis_1/total_area
          elif side == 'left' or side == 'right': 
               distance_from_edge: float = first_moment_axis_2/total_area

          
          return distance_from_edge

                         


@dataclass
class ReinforcedConcreteBeamSection(ReinforcedConcreteSection): 
    
     def __post_init__(self) -> None:
          super().__init__

     
     def get_gross_inertia(self, axis: Literal[1, 2]): 
          if axis == 1: 
               inertia: float = self.ConcreteSection.width * self.ConcreteSection.height**3 / 12
          elif axis == 2: 
               inertia: float = self.ConcreteSection.height * self.ConcreteSection.width**3 / 12

          return inertia
     
     def get_positive_nominal_moment(self): 
          fc: float = self.ConcreteSection.Concrete.compression_strength
          beta_1: float = self.ConcreteSection.Concrete.beta_1
          b: float = self.ConcreteSection.Section.width 
          d_bottom: float = self.ConcreteSection.Section.height - self.get_flexural_coord_from_edge('bottom')
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
     