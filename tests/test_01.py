import core.sections as sections
import core.sections as sections
import core.materials as materials
import core.analysis as analysis

if __name__ == "__main__": 
     Concrete_28 = materials.Concrete(
          compression_strength=28
     )

     Steel_420 = materials.Steel(
          tension_strength=420
     )


     RCB_30X60 = sections.RCRectangularBeamSection(
          Concrete=Concrete_28, 
          Steel=Steel_420, 
          width=300, 
          height=600,
          flexural_top_steel_area=1521,
          flexural_bottom_steel_area=1014,
          shear_steel_area=142,
          shear_steel_separation=50
     )


     print(0.9*RCB_30X60.get_nominal_moment(axis=2, sign='positive'), "N-mm", "M+")
     print(0.9*RCB_30X60.get_nominal_moment(axis=2, sign='negative'), "N-mm", "M+")
     # print(RCB_30X60_1014_1014.get_nominal_shear_strength_for_positive_moment(), "V")
     # print(RCB_30X60_1014_1014.get_nominal_shear_strength_for_negative_moment(), "V-")
     # print(RCB_30X60_1014_1014.get_ultimate_shear_limit_for_positive_moment(), "Vu+")

     # print(RCB_30X60_1014_1014.__repr__())