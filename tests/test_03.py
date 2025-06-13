# Solve the cantilever beam. With DEAD Load and Live laod. 
import core.fem.elements as elements 
import core.structural_sections as structural_sections
import core.materials as materials 
import core.geometry as geometry
import pandas as pd 

if __name__ == "__main__": 
     print("Hello. This module should run")
     Concrete28 = materials.Concrete(compression_strength=28)
     Steel420 = materials.Steel(tension_strength=420)
     
     S120X250 = geometry.RectangularSection(
          width=120, 
          height=250,
     )

     RCB120X250 = structural_sections.RCRectangularBeamSection(
          Concrete=Concrete28,
          Steel=Steel420,
          Section=S120X250
     )

     Cantilever= elements.B2D2(
          nodes=[
               (0, 0), 
               (2000, 0)
          ],
          ReinforcedSection=RCB120X250
     )

     Forces

     Restrains
     print(pd.DataFrame(Cantilever.stiffness_matrix))
     print(materials.Concrete(28).elastic_modulus)