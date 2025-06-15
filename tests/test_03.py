# Solve the cantilever beam. With DEAD Load and Live laod. 
import core.fem.elements as elements 
import core.structural_sections as structural_sections
import core.materials as materials 
import core.geometry as geometry
import core.fem.elements as elements
import pandas as pd 
import core.fem.forces as forces
import core.fem.restrains as restrain 
import core.fem.model as model

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

     P01 = elements.Node(
          coordinates=(0, 0, 0)
     )

     P02 = elements.Node(
          coordinates=(2000, 0, 0)
     )
     Cantilever= elements.B2D2(
          nodes=(P01, P02),
          ReinforcedSection=RCB120X250
     )

     Force = forces.PunctualForceOnBeams(
          load_case="DEAD",
          magnitud=-2000, 
          axis=(3, 'local'),
          position=1,
          elements=[Cantilever]
     )

     Restrain = restrain.FixedSupport(
          node=P01
     )
     

     M = model.LinearElastic(
          active_dofs=(True, True, False, False, False, True),
          elements=[Cantilever],
          restrains=[Restrain],
          loads=[Force]
     )

     print(pd.Series(M.solve()))
     print(pd.DataFrame(Cantilever.stiffness_matrix))
     print(materials.Concrete(28).elastic_modulus)

     print(pd.DataFrame(Cantilever.alt_stiffness_matrix))