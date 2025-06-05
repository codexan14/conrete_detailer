import elements
import materials
# Tomar el momento de una viga B30X60, 3 barras abajo de 1 y dos barras arriba de 1"
#

Concrete_24 = materials.Concrete(
     compression_resistance=24
)

Steel_420 = materials.Steel(
     yield_stress=420
)

CS_30X60 = elements.ConcreteSection(
     width=300, 
     height=600, 
     Concrete=Concrete_24
)

SR_1014 = elements.Rebar(
     diameter=25, 
     quantity=2,
     Steel=Steel_420
)

SS_142_100 = elements.Stirrup(
     diameter=10, 
     quantity=2,
     spacing=100,
     Steel=Steel_420
)

RCB_30X60_1014_1014 = elements.ReinforcedConcreteBeamSection(
     ConcreteSection = CS_30X60, 
     TopRebar= SR_1014, 
     BottomRebar= SR_1014,
     Stirrup=SS_142_100
)

print(RCB_30X60_1014_1014.get_positive_nominal_moment())