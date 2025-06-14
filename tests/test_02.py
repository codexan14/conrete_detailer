# BEAM IN FEM, ANALYSIS
import core.fem.elements as elements 
import core.geometry as geometry
import core.structural_sections as structural_section
import core.materials as materials
import core.fem.elements as elements
import pandas as pd 

if __name__ == '__main__':
     Concrete24 = materials.Concrete(
          compression_strength = 28
     )

     Steel420 = materials.Steel(
          tension_strength=420
     )

     S300X600 = geometry.RectangularSection(
          width=300, 
          height=600
     )

     RCB300X600 = structural_section.RCRectangularBeamSection(
          Concrete=Concrete24, 
          Steel=Steel420,
          Section = S300X600
     )

     P1 = elements.Node(
          coordinates=(0, 0, 0)
     )

     P2 = elements.Node(
          coordinates=(10000, 0, 0)
     )
     FEMBEam = elements.B2D2(
          nodes = (P1, P2), 
          ReinforcedSection=RCB300X600
     )
     

     print(pd.DataFrame(FEMBEam.stiffness_matrix))