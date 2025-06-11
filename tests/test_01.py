import core.composed_sections as composed_sections
import core.sections as sections
import core.materials as materials

if __name__ == "__main__": 
     Concrete_28 = materials.Concrete(
          compression_strength=28
     )

     Steel_420 = materials.Steel(
          tension_strength=420
     )

     S_30X60 = sections.RectangularSection(
          width=300, 
          height=600
     )

     CS_30X60 = composed_sections.ConcreteSection(
          Section=S_30X60,
          Concrete=Concrete_28
     )

     
     SRT_1014 = composed_sections.FlexuralSteel(
          position='top',
          diameter=25,
          quantity=2
     )

     SRB_1014 = composed_sections.FlexuralSteel(
          position='bottom',
          diameter=25,
          quantity=2
     )

     SS_142_100 =composed_sections.Stirrups(
          position='stirrups', 
          diameter=25, 
          quantity=2,
          stirrup_type='closed'
     )
     

     RCB_30X60_1014_1014 = composed_sections.ReinforcedConcreteBeamSection(
          ConcreteSection=CS_30X60,
          flexural_steel_list=[SRT_1014, SRB_1014], 
          stirrups_list=[SS_142_100]
     )

     print(0.9*RCB_30X60_1014_1014.get_positive_nominal_moment(), "N-mm", "M+")
     # print(0.9*RCB_30X60_1014_1014.get_negative_nominal_moment(), "N-mm", "M-")
     # print(RCB_30X60_1014_1014.get_nominal_shear_strength_for_positive_moment(), "V")
     # print(RCB_30X60_1014_1014.get_nominal_shear_strength_for_negative_moment(), "V-")
     # print(RCB_30X60_1014_1014.get_ultimate_shear_limit_for_positive_moment(), "Vu+")

     # print(RCB_30X60_1014_1014.__repr__())