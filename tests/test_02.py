from typing import Literal
from core.materials import Concrete, Steel
from core.composed_sections import ConcreteSection, ReinforcedConcreteSection, ReinforcedConcreteBeamSection



if __name__ == "__main__":
     print("DEBUG: Imports successful!") # <-- Add this after imports

     Concrete_28 = Concrete(
          compression_strength=28
     )

     Steel_420 = Steel(
          tension_strength=420
     )

     CS_30X60 = ConcreteSection(
          width=300, 
          height=600, 
          Concrete=Concrete_28
     )

     CornerBars = Rebar(
          diameter=25, 
          quantity=4,
          Steel=Steel_420
     )

     HorizontalRebar = Rebar(
          diameter=25, 
          quantity=4,
          Steel=Steel_420
     )

     VerticalRebar = Rebar(
          diameter=25, 
          quantity=4,
          Steel=Steel_420
     )

     SS_142_100 = Stirrup(
          diameter=9.5, 
          quantity=2,
          spacing=50,
          Steel=Steel_420
     )


     C1 = ReinforcedConcreteColumnSection(
          ConcreteSection=CS_30X60, 
          CornerRebar=CornerBars, 
          HorizontalRebar=HorizontalRebar, 
          VerticalRebar=VerticalRebar,
          Stirrup=SS_142_100
     )


     print(C1.horizontal_spacing)