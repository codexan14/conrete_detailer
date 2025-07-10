from core.cost import *

if __name__ == "__main__":
    B300X600_1 = Beam(
        width=300,
        height=600,
        length=1000, 
        concrete_resistance=28,
        TopRebar=LongitudinalRebar(
            diameter=25, 
            quantity=5, 
            length=2,
            start_hook_degree=90,
            end_hook_degree=0
        ),
        BotttomRebar=LongitudinalRebar(
            diameter=25, 
            quantity=5, 
            length=2,
            start_hook_degree=90,
            end_hook_degree=0
        ),
        SkinRebar=LongitudinalRebar(
            diameter=25, 
            quantity=5, 
            length=2,
            start_hook_degree=90,
            end_hook_degree=0
        ),
        AdditionalTopRebarStart=LongitudinalRebar(
            diameter=25, 
            quantity=5, 
            length=2,
            start_hook_degree=90,
            end_hook_degree=0
        ),
        AdditionalTopRebarEnd=LongitudinalRebar(
            diameter=25, 
            quantity=5, 
            length=2,
            start_hook_degree=90,
            end_hook_degree=0
        ),
        AdditionalTBottomRebar=LongitudinalRebar(
            diameter=25, 
            quantity=5, 
            length=2,
            start_hook_degree=90,
            end_hook_degree=0
        )
    )

    print(B300X600_1._Concrete)