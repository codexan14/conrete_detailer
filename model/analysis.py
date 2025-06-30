from typing import Literal, Any
import argparse

def get_nominal_moment(
          fc: float, 
          fy: float,
          b:float, 
          As_top:float, 
          d_top:float, 
          As_bottom:float, 
          d_bottom:float,
          beta_1: float = 0.85)->float: 

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
     

# # def get_minimum_shear_reinforcement(self) -> float: #Av_min/s
# #      fc: float = self.ConcreteSection.Concrete.compression_resistance 
# #      b: float = self.ConcreteSection.width
# #      fyt: float = self.Stirrup.Steel.yield_stress

# #      minimum_steel_reinforcement: float =max(0.062*math.sqrt(fc), 0.35)*b/fyt # mm^2 / mm

# #      return minimum_steel_reinforcement

# # def get_nominal_concrete_shear_strength_for_positive_moment(self) -> float: 
# #      Av_min: float = self.get_minimum_shear_reinforcement()
# #      Av: float = self.Stirrup.area/self.Stirrup.spacing 
# #      d_bottom: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge
# #      fc: float = self.ConcreteSection.Concrete.compression_resistance
# #      b: float = self.ConcreteSection.width
# #      As_bottom = self.BottomRebar.area 
     
# #      # Lambda_ calculation 
# #      lambda_ = 1.00 #NOT LIGHTWEIGHT CONCRETE 
# #      lambda_s = min(1, math.sqrt(2/(1+0.004*d_bottom)))

# #      # Comparison
# #      if Av >= Av_min: 
# #           nominal_concrete_shear_strength: float = 0.17*lambda_*math.sqrt(fc)*b*d_bottom
# #      else: 
# #           nominal_concrete_shear_strength: float = 0.66*lambda_s*lambda_*(As_bottom/(b*d_bottom))**(1/3) * math.sqrt(fc)*b*d_bottom

# #      return nominal_concrete_shear_strength

# # def get_nominal_concrete_shear_strength_for_negative_moment(self) -> float: 
# #      Av_min: float = self.get_minimum_shear_reinforcement()
# #      Av: float = self.Stirrup.area/self.Stirrup.spacing 
# #      d_top: float = self.ConcreteSection.height - self.top_rebar_position_from_edge
# #      fc: float = self.ConcreteSection.Concrete.compression_resistance
# #      b: float = self.ConcreteSection.width
# #      As_top: float = self.TopRebar.area 

# #      # Lambda_ calculation 
# #      lambda_ = 1.00 #NOT LIGHTWEIGHT CONCRETE 
# #      lambda_s = min(1, math.sqrt(2/(1+0.004*d_top)))

# #      # Comparison
# #      if Av >= Av_min: 
# #           nominal_concrete_shear_strength: float = 0.17*lambda_*math.sqrt(fc)*b*d_top

# #      else: 
# #           nominal_concrete_shear_strength: float = 0.66*lambda_s*lambda_*(As_top/(b*d_top))**(1/3) * math.sqrt(fc)*b*d_top

# #      return nominal_concrete_shear_strength

# # def get_nominal_stirrups_shear_strength_for_positive_moment(self) -> float: 
# #      Av: float = self.Stirrup.area
# #      d_bottom: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge
# #      fyt: float = self.Stirrup.Steel.yield_stress 
# #      s: float = self.Stirrup.spacing

# #      return Av*fyt*d_bottom/s

# # def get_nominal_stirrups_shear_strength_for_negative_moment(self) -> float: 
# #      Av: float = self.Stirrup.area
# #      d_top: float = self.ConcreteSection.height - self.top_rebar_position_from_edge
# #      fyt: float = self.Stirrup.Steel.yield_stress 
# #      s: float = self.Stirrup.spacing

# #      return Av*fyt*d_top/s

# # def get_ultimate_shear_limit_for_positive_moment(self) -> float: 
# #      phi:float = 0.60 #Shear

# #      fc: float = self.ConcreteSection.Concrete.compression_resistance 
# #      b: float = self.ConcreteSection.width 
# #      d_bottom: float = self.ConcreteSection.height - self.bottom_rebar_position_from_edge

# #      Vc: float = self.get_nominal_concrete_shear_strength_for_positive_moment()

# #      return phi*(Vc + 0.66*math.sqrt(fc)*b*d_bottom)

# # def get_ultimate_shear_limit_for_negative_moment(self) -> float: 
# #      phi:float = 0.60 #Shear

# #      fc: float = self.ConcreteSection.Concrete.compression_resistance 
# #      b: float = self.ConcreteSection.width 
# #      d_top: float = self.ConcreteSection.height - self.top_rebar_position_from_edge

# #      Vc: float = self.get_nominal_concrete_shear_strength_for_negative_moment()

# #      return phi*(Vc + 0.66*math.sqrt(fc)*b*d_top)

# # def get_nominal_shear_strength_for_positive_moment(self): 
# #      Vc: float = self.get_nominal_concrete_shear_strength_for_positive_moment()
# #      Vs: float = self.get_nominal_stirrups_shear_strength_for_positive_moment() 

# #      return Vc + Vs

# # def get_nominal_shear_strength_for_negative_moment(self): 
# #      Vc: float = self.get_nominal_concrete_shear_strength_for_negative_moment()
# #      Vs: float = self.get_nominal_stirrups_shear_strength_for_negative_moment() 
     
# #      return Vc + Vs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramientas de análisis estructural")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: moment
    moment_parser = subparsers.add_parser("moment", help="Calcular momento nominal")
    moment_parser.add_argument("--fc", type=float)
    moment_parser.add_argument("--fy", type=float)
    moment_parser.add_argument("--b", type=float)
    moment_parser.add_argument("--d_top", type=float)
    moment_parser.add_argument("--As_top", type=float)
    moment_parser.add_argument("--d_bottom", type=float)
    moment_parser.add_argument("--As_bottom", type=float)

    # Subcommand: shear
    shear_parser = subparsers.add_parser("shear", help="Calcular resistencia a cortante")
    shear_parser.add_argument("Vc", type=float)
    shear_parser.add_argument("Vs", type=float)

    args = parser.parse_args()

    if args.command == "moment":
        Mn = get_nominal_moment(args.fc, args.fy, args.b, args.As_top, args.d_top, args.As_bottom, args.d_bottom)
        print(f"Mn = {Mn:.2f} N·cm")


    elif args.command == "shear":
        V = get_shear_capacity(args.Vc, args.Vs)
        print(f"V = {V:.2f} N")