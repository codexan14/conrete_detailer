import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from typing import Literal
from dataclasses import dataclass, field

from streamlit.delta_generator import DeltaGenerator

SUPPORT_CONDITIONS: list[str] = ["free", "simple supported", "fixed"]
SUPPORT_CONDITIONS_TYPE = Literal["free", "simple supported", "fixed"]



def restrained_dof(first_support: SUPPORT_CONDITIONS_TYPE, second_support: SUPPORT_CONDITIONS_TYPE)-> int:  
    first_support_value: int 
    second_support_value: int 

    if first_support == "free": 
        first_support_value = 0
    elif first_support == "simple supported":
        first_support_value = 1
    elif first_support == "fixed": 
        first_support_value = 2
    else: 
        first_support_value = 0
    
    if second_support == "free": 
        second_support_value = 0
    elif second_support == "simple supported":
        second_support_value = 1
    elif second_support == "fixed": 
        second_support_value = 2
    else: 
        second_support_value = 0
    
    return first_support_value + second_support_value

def beam_type(first_support: Literal["free", "simple supported", "fixed"], second_support: Literal["free", "simple supported", "fixed"]) -> Literal['Cantilever'] | Literal['Simple Supported'] | Literal['One End Fixed'] | Literal['Both Ends Fixed'] | Literal['Partially Stable'] | Literal['Unstable']:

    if (
        ((first_support == "free") and (second_support == "fixed")) or ((first_support == "fixed") and (second_support == "free"))
        ):
        st.text("CANTILEVER")
        return "Cantilever"

    if (
        (first_support == "simple supported") and (second_support == "simple supported")
        ):
        st.text("Simple Supported")
        return "Simple Supported"
    
    if (
        ((first_support == "simple supported") and (second_support == "fixed")) or ((first_support == "fixed") and (second_support == "simple supported"))
        ): 
        st.text("One End Fixed")
        return "One End Fixed" 
    
    if ((first_support == "fixed") and (second_support == "fixed")): 
        st.text("Both Ends Fixed")
        return "Both Ends Fixed" 
    
    if (
        ((first_support == "free") and (second_support == "simple supported")) or ((first_support == "simple supported") and (second_support == "free"))
        ):
        st.text("Partially Stable")
        return "Partially Stable"

    
    st.text("Unknown")
    return "Unstable"
    
@dataclass
class Slab: 
    left_side_support: Literal["free", "simple supported", "fixed"]
    right_side_support: Literal["free", "simple supported", "fixed"]
    bottom_side_support: Literal["free", "simple supported", "fixed"]
    top_side_support: Literal["free", "simple supported", "fixed"]
    horizontal_length: float 
    vertical_length: float 
    condition: Literal['Unstable'] | Literal['1D Vertical'] | Literal['1D Horizontal'] | Literal['2D'] | Literal[''] = field(init=False)
    condition_axis_1: Literal['Cantilever'] | Literal['Simple Supported'] | Literal['One End Fixed'] | Literal['Both Ends Fixed'] | Literal['Partially Stable'] | Literal['Unstable'] = field(init=False)
    condition_axis_2: Literal['Cantilever'] | Literal['Simple Supported'] | Literal['One End Fixed'] | Literal['Both Ends Fixed'] | Literal['Partially Stable'] | Literal['Unstable'] = field(init=False)

    def __post_init__(self) -> None: 
        
        self.condition_axis_1 = beam_type(self.left_side_support, self.right_side_support)
        self.condition_axis_2 = beam_type(self.bottom_side_support, self.top_side_support)
        self.condition = self.get_direction()

    
    def get_direction(self) -> Literal['Unstable'] | Literal['1D Vertical'] | Literal['1D Horizontal'] | Literal['2D'] | Literal['']:
    
        condition: str = ""
        if ((self.condition_axis_1 == "Unstable") or (self.condition_axis_1 == "Partially Stable")) and ((self.condition_axis_2 == "Unstable") or (self.condition_axis_2 == "Partially Stable")): 
            condition = "Unstable"
        elif self.condition_axis_1 != "Unstable" and self.condition_axis_2 == "Unstable": 
            condition = "1D Horizontal"
        elif self.condition_axis_1 == "Unstable" and self.condition_axis_2 != "Unstable": 
            condition = "1D Vertical"
        else: #self.condition_axis_1 != "Unstable" and self.condition_axis_2 != "Unstable": 
            if self.horizontal_length / self.vertical_length <= 0.5: 
                condition = "1D Horizontal"
            elif self.horizontal_length / self.vertical_length <= 2: 
                condition = "2D"
            else: 
                condition = "1D Vertical"

        return condition
    

    def get_minimum_width(self) -> float | Warning:

        if roof_type_check:
            denominator: dict[str, int] = {
            "Cantilever": 10, 
            "Simple Supported": 20, 
            "One End Fixed": 24, 
            "Both Ends Fixed": 28,
            "Partially Stable": 1,
            "Unstable": 1
        }
        else: 
            denominator: dict[str, int] = {
                "Cantilever": 7, 
                "Simple Supported": 14, 
                "One End Fixed": 16, 
                "Both Ends Fixed": 19,
                "Partially Stable": 1,
                "Unstable": 1
            }

        k_hor: int = denominator[beam_type(self.left_side_support, self.right_side_support)]

        k_ver: int = denominator[beam_type(self.bottom_side_support, self.top_side_support)]
        
        if self.condition == "1D Vertical" and self.condition_axis_2 != "Unstable" and self.condition_axis_2 != "Partially Stable": 
            return self.vertical_length / k_ver
        elif self.condition == "1D Horizontal" and self.condition_axis_1 != "Unstable" and self.condition_axis_1 != "Partially Stable":
            return self.horizontal_length / k_hor
        elif self.condition == "2D": 
            beta: float = max(self.horizontal_length, self.vertical_length) / min(self.horizontal_length, self.vertical_length)
            return max(self.vertical_length, self.horizontal_length)/(30 + 3*beta)
        else: 
            st.warning("The Slab is Probably Unstable")
            return 0

st.set_page_config(layout="wide")

height = st.sidebar.slider(label="Input Height", min_value=100, max_value=2000, value=500)


input_checkbox: bool = st.sidebar.checkbox(label = "Show Input")
output_checkbox: bool = st.sidebar.checkbox(label = "Show Output")

input_col, output_col = st.columns([1,1])

# --- Columna izquierda: Inputs ---
with input_col:
    st.header("Inputs")
    with st.container(height=height):
        st.subheader("Support Conditions")
        support_column = st.columns(2)
        
        with support_column[0]:
            support_condition_left: str = st.selectbox(
                label="Left Side Support Condition", 
                options=["free", "simple supported", "fixed"]
            )

            support_condition_right: str = st.selectbox(
                label="Right Side Support Condition", 
                options=["free", "simple supported", "fixed"]
            )

        with support_column[1]:
            support_condition_top: str = st.selectbox(
                label="Top Side Support Condition", 
                options=["free", "simple supported", "fixed"]
            )

            support_condition_bottom: str = st.selectbox(
                label="Bottom Side Support Condition", 
                options=["free", "simple supported", "fixed"]
            )
        
        st.subheader("Support Conditions")
        length_column: list[DeltaGenerator] = st.columns(2)

        with length_column[0]:
            horizontal_length: float = st.number_input(
                label="Horizontal Length (m)", 
                min_value=0.10, 
                max_value=50.0,
                step=0.10)

        with length_column[1]:
            vertical_length: float = st.number_input(
                label="Vertical Length (m)", 
                min_value=0.10, 
                max_value=50.0,
                step=0.10
                )
        
        st.subheader("Slab Type")
        roof_type_check: bool = st.checkbox("Is it a roof?")


# --- Columna derecha: Outputs ---
MySlab = Slab(
            left_side_support=support_condition_left,
            right_side_support=support_condition_right,
            bottom_side_support=support_condition_bottom,
            top_side_support=support_condition_top,
            horizontal_length=horizontal_length,
            vertical_length=vertical_length
        )

with output_col:
    st.header("Outputs")
    with st.container(height=height):
        st.subheader("Support Conditions") 
        st.write(f"Axis 1: {MySlab.condition_axis_1}")
        st.write(f"Axis 2: {MySlab.condition_axis_2}")

        st.subheader("Direction")
        st.write(f"{MySlab.condition}")
        st.subheader("Recommended Width")

        recommended_width: float = MySlab.get_minimum_width()

        st.metric("Recommended Width", value=recommended_width)

