import streamlit as st 
import numpy as np 
import pandas as pd 
import plotly.graph_objects as go
import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

print("sys.path en interaction_diagram.py:")
for p in sys.path:
    print(p)


import core.analysis.flexuralcompression
from core.geometry import bar_area, circle_perimeter

st.set_page_config(layout="wide")

container_height = st.sidebar.slider(label="Input Height", min_value=100, max_value=2000, value=500)


input_checkbox: bool = st.sidebar.checkbox(label = "Show Input")
output_checkbox: bool = st.sidebar.checkbox(label = "Show Output")

st.markdown("# Reinforced Concrete Interaction Diagram")
input_col, output_col = st.columns([1,1])

with input_col: 
    st.markdown("## Input Section")
    with st.container(height=container_height):

        st.markdown("### Material")
        column_1, column_2 = st.columns(2)
        with column_1:
            fc = st.number_input(label="Concrete Compression Strength [MPa]", min_value=20, max_value=100)
        
        with column_2: 
            fy = st.number_input(label="Steel Yield Stress", min_value=420, max_value=1000)
        
        st.markdown("### Concrete Section")
        column_3, column_4 = st.columns(2)
        with column_3:
            base = st.number_input(label="Base [mm]", min_value=200, max_value=3000, step = 50)
        with column_4: 
            height = st.number_input(label="Height [mm]", min_value=200, max_value=3000, step = 50)
        
        st.markdown("### Reinforcement")

        column_5, column_6 = st.columns(2)
        with column_5: 
            corner_bars_diameter = st.number_input(label="Corner Bars Diameter [mm]", step = 1)
            inner_bars_diameter = st.number_input(label="Inner Bars Diameter [mm]", step = 1)
            horizontal_bars_number = st.number_input(label=" Number of bars (horizontal direction) between corner bars [mm]", step = 1)
            vertical_bars_number = st.number_input(label=" Number of bars (vertial direction) between corner bars [mm]", step = 1)

        with column_6: 
            number_of_rows = vertical_bars_number+2
            st.metric("Number of rows", number_of_rows, border=True)

            spacing_y = (height - 2*40 - 2*10 - 2*12.5)/(vertical_bars_number+1)
            st.metric("spacing_y", f"{spacing_y:.2f}", border=True)

            spacing_x = (base - 2*40 - 2*10 - 2*12.5)/(horizontal_bars_number+1)
            st.metric("spacing_x", f"{spacing_x:.2f}", border=True)
            
            steel_areas = np.zeros(number_of_rows)
            steel_areas = steel_areas + 2*bar_area(inner_bars_diameter)
            steel_areas[0] = 2*bar_area(corner_bars_diameter) + 2*horizontal_bars_number*bar_area(inner_bars_diameter)
            steel_areas[-1] = steel_areas[0]
            
            st.metric("Total Area", f"{np.sum(steel_areas):.2f}", border=True)
        st.table(
            {"Area [mm2]": steel_areas,
             "Position [mm]": [40+10+12.5 + spacing_y*i for i in range(len(steel_areas))]
             })

Pn, Mn, phiPn, phiMn = core.analysis.flexuralcompression.interaction_diagram(
    base, height, fc, fy, rebar_areas=np.array(steel_areas), n=20)

fig_1 = go.Figure()
fig_1.add_trace(go.Scatter(x=Mn, y=Pn, mode='lines', name='Interaction Diagram'))
fig_1.add_trace(go.Scatter(x=phiMn, y=phiPn, mode='lines', name='Reduced Interaction Diagram'))
fig_1.update_layout(
    title='Interaction Diagram',
    xaxis_title='Moment [N-mm]',
    yaxis_title='Force [N]',
    template='plotly_dark',
    legend=dict(x=0, y=1)
)

fig_2 = go.Figure()
fig_2.add_trace(go.Scatter(x = [0, base, base ,0, 0], y = [0, 0, height, height, 0]))
fig_2.add_trace(go.Scatter(
    x = [40+10+12.5, base - 40-10-12.5, base - 40-10-12.5, 40+10+12.5, 40+10+12.5], 
    y = [40+10+12.5, 40+10+12.5, height-40-10-12.5, height-40-10-12.5, 40+10+12.5],
    mode="markers",
    marker=dict(
        size=corner_bars_diameter, 
        color = "black")))

for i in range(horizontal_bars_number):
    fig_2.add_trace(go.Scatter(
        x = [40 + 10 + 12.5 + spacing_x*(i+1)], 
        y = [40 + 10 + 12.5], 
        marker=dict(size=inner_bars_diameter, color = "black")))
    
    fig_2.add_trace(go.Scatter(
        x = [40 + 10 + 12.5 + spacing_x*(i+1)], 
        y = [height - 40 - 10 - 12.5], 
        marker=dict(size=inner_bars_diameter, color = "black")))

for i in range(vertical_bars_number):
    fig_2.add_trace(go.Scatter(
        x = [40 + 10 + 12.5],
        y = [40 + 10 + 12.5 + spacing_y*(i+1)], 
        marker=dict(size=inner_bars_diameter, color = "black")))
    
    fig_2.add_trace(go.Scatter(
        x = [base - 40 - 10 - 12.5], 
        y = [40 + 10 + 12.5 + spacing_y*(i+1)], 
        marker=dict(size=inner_bars_diameter, color = "black")))

fig_2.update_layout(xaxis=dict(scaleanchor='y', scaleratio=1))

with output_col:
    st.markdown("## Output")
    box = st.selectbox(
            label="Select Output",
            options=["Interaction Diagram", "Column Section"])
    with st.container(height=container_height):
        if box == "Interaction Diagram":
            st.plotly_chart(fig_1)
        elif box == "Column Section":
            st.plotly_chart(fig_2)