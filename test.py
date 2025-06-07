import elements
import materials

Concrete_28 = materials.Concrete(
     compression_resistance=28
)

Steel_420 = materials.Steel(
     yield_stress=420
)

CS_30X60 = elements.ConcreteSection(
     width=300, 
     height=600, 
     Concrete=Concrete_28
)

SR_1014 = elements.Rebar(
     diameter=25, 
     quantity=2,
     Steel=Steel_420
)

SR_2028 = elements.Rebar(
     diameter=25, 
     quantity=4,
     Steel=Steel_420
)

SS_142_100 = elements.Stirrup(
     diameter=9.5, 
     quantity=2,
     spacing=50,
     Steel=Steel_420
)

RCB_30X60_1014_1014 = elements.ReinforcedConcreteBeamSection(
          ConcreteSection = CS_30X60, 
          TopRebar= SR_1014, 
          BottomRebar= SR_1014,
          Stirrup=SS_142_100
     )

print(0.9*RCB_30X60_1014_1014.get_positive_nominal_moment(), "N-mm", "M+")
print(0.9*RCB_30X60_1014_1014.get_negative_nominal_moment(), "N-mm", "M-")
print(RCB_30X60_1014_1014.get_nominal_shear_strength_for_positive_moment(), "V")
print(RCB_30X60_1014_1014.get_nominal_shear_strength_for_negative_moment(), "V-")
print(RCB_30X60_1014_1014.get_ultimate_shear_limit_for_positive_moment(), "Vu+")

# print(RCB_30X60_1014_1014.__repr__())