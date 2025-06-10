import streamlit as st 
import elements
import materials

def main():
     st.title("BEAM APP")
     st.header("Input Section")

     #Defining the materials
     st.subheader("Materials")
     concrete_compression_resistance=st.number_input(label="Concrete compression strength [MPa]", min_value=21.0, step=1.00)
     steel_yield_stress=st.number_input(label="Steel yield stress [MPa]", min_value=420.0, step = 10.00)
     Concrete_material = materials.Concrete(
          compression_resistance=concrete_compression_resistance
     )

     Steel_material = materials.Steel(
          yield_stress=steel_yield_stress
     )
     ###### SCRIPT

     st.subheader("Concrete Section Properties")
     width: int=st.number_input("Beam width [mm]: ", min_value=100, step=10)
     height: int=st.number_input("Beam height [mm]: ", min_value=100, step=10)

     ConcreteSection = elements.ConcreteSection(
          width=width, 
          height=height, 
          Concrete=Concrete_material
     )

     st.subheader("Top Rebar Properties")
     col1, col2= st.columns(2)
     with col1:
          top_rebar_diameter: int=st.number_input("Top Rebar Diameter [mm]", min_value=1, step=1)
     with col2:
          top_rebar_quantity: int=st.number_input("Number of Top bars", min_value=1, step=1) 

     TopRebar = elements.Rebar(
          diameter=top_rebar_diameter, 
          quantity=top_rebar_quantity,
          Steel=Steel_material
     )

     st.subheader("Bottom Rebar Properties")
     col1, col2= st.columns(2)
     with col1:
          bottom_rebar_diameter: int=st.number_input("bottom Rebar Diameter [mm]", min_value=1, step=1)
     with col2:
          bottom_rebar_quantity: int=st.number_input("Number of Bottom bars", min_value=1, step=1) 

     BottomRebar = elements.Rebar(
<<<<<<< HEAD
<<<<<<< HEAD
          diameter=bottom_rebar_diameter, 
          quantity=bottom_rebar_quantity,
=======
          diameter=top_rebar_diameter, 
          quantity=top_rebar_quantity,
>>>>>>> 6d872a8 (feat: Added the GUI with streamlit and the Beam class can now calculate nominal strengths)
=======
          diameter=bottom_rebar_diameter, 
          quantity=bottom_rebar_quantity,
>>>>>>> 7c22ff0 (Modified the license)
          Steel=Steel_material
     )


     st.subheader("Stirrups")

     col1, col2, col3= st.columns(3)
     with col1:
          stirrup_diameter: int=st.number_input("Stirrup Diameter [mm]", min_value=1, step=1)
     with col2:
          stirrup_legs: int=st.number_input("Number of legs", min_value=1, step=1) 
     with col3:
          stirrup_spacing: int=st.number_input("Spacing", min_value=1, step=1) 


     Stirrup = elements.Stirrup(
          diameter=stirrup_diameter, 
          quantity=stirrup_legs,
          spacing=stirrup_spacing,
          Steel=Steel_material
     )

     RCB = elements.ReinforcedConcreteBeamSection(
               ConcreteSection = ConcreteSection, 
               TopRebar= TopRebar, 
               BottomRebar= BottomRebar,
               Stirrup=Stirrup
          )

     st.header("Results")
     st.subheader("Flexural Capacity")

     table = {
          "Names": [
               "Positive Nominal Moment", 
               "Negative Nominal Moment", 
               "Reduction Factor", 
               "Reduced Positive Nominal Moment", 
               "Reduced Negative Nominal Moment"
               ],
          "Variables": [
               "Mn [+]", 
               "Mn [-]", 
               "φ", 
               "φMn [+]", 
               "φMn [-]"],
          "Values": [
               f"{RCB.get_positive_nominal_moment():.2f} N-mm", 
               f"{RCB.get_negative_nominal_moment():.2f} N-mm", 
               f"{0.90:.2f}", 
               f"{0.90*RCB.get_positive_nominal_moment():.2f} N-mm", 
               f"{0.90*RCB.get_negative_nominal_moment():.2f} N-mm"],
     }

     st.table(data=table)
     # print(0.9*RCB_30X60_1014_1014.get_positive_nominal_moment(), "N-mm", "M+")
     # print(0.9*RCB_30X60_1014_1014.get_negative_nominal_moment(), "N-mm", "M-")
     # print(RCB_30X60_1014_1014.get_nominal_shear_strength_for_positive_moment(), "V")
     # print(RCB_30X60_1014_1014.get_nominal_shear_strength_for_negative_moment(), "V-")
     # print(RCB_30X60_1014_1014.get_ultimate_shear_limit_for_positive_moment(), "Vu+")


if __name__ == "__main__":
    main()