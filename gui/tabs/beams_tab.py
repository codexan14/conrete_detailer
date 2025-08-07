import tkinter as tk
import tkinter.ttk as ttk
from core.utils import extract_column_from_csv
from core.beam_lrfd import calculate_beam_positive_moment_capacity, calculate_beam_negative_moment_capacity
import csv 
from typing import Iterator, cast
import pandas as pd 

class BeamModule:
    def __init__(self, path_to_folder: tk.StringVar) -> None: 
        self.beams_tab = ttk.Frame()
        self.path_to_folder: tk.StringVar = path_to_folder
        
        # Variables
        self.path_to_folder: tk.StringVar = path_to_folder        
        # Widgets
        #ttk.Label(master=self.beams_tab, textvariable=self.path_to_file).grid(column=0, row=0)
        ttk.Button(master=self.beams_tab, text="Flexural", command=self.calculate).grid(column=1, row=1)

    def update_path_to_file(self):
        self.path_to_file: str = self.path_to_folder.get() + "/beam_sections.csv"

    def calculate(self) -> None: 
        self.update_path_to_file() 
        data: pd.DataFrame = pd.read_csv(filepath_or_buffer=self.path_to_file, sep=',') #type: ignore

        positive_nominal_moment: list[float] = [0]*len(data["base"])
        negative_nominal_moment: list[float] = [0]*len(data["base"])
        flexural_reduction_factor: list[float] = [0]*len(data["base"])

        for base, height, concrete_strength, rebar_area_top, rebar_area_bottom, rebar_position_top, rebar_position_bottom, i in zip(
            data["base"], 
            data["height"], 
            data["concrete_strength"], 
            data["rebar_area_top"],
            data["rebar_area_bottom"],
            data["rebar_position_top"],
            data["rebar_position_bottom"],
            range(len(data["base"]))
        ):

            positive_nominal_moment[i] = calculate_beam_positive_moment_capacity(
                base=base, 
                height=height, 
                concrete_strength=concrete_strength, 
                rebar_area_top = rebar_area_top, 
                rebar_area_bottom=rebar_area_bottom, 
                rebar_position_top=rebar_position_top, 
                rebar_position_bottom=rebar_position_bottom)
            
            negative_nominal_moment[i] = calculate_beam_negative_moment_capacity(
                base=base, 
                height=height, 
                concrete_strength=concrete_strength, 
                rebar_area_top = rebar_area_top, 
                rebar_area_bottom=rebar_area_bottom, 
                rebar_position_top=rebar_position_top, 
                rebar_position_bottom=rebar_position_bottom)
            
            flexural_reduction_factor[i] = 0.90
        
        data["positive_nominal_moment"] = positive_nominal_moment
        data["negative_nominal_moment"] = negative_nominal_moment
        data["flexural_reduction_factor"] = flexural_reduction_factor
        data["positive_phi*Mn"] = data["positive_nominal_moment"] * data["flexural_reduction_factor"]
        data["negative_phi*Mn"] = data["negative_nominal_moment"] * data["flexural_reduction_factor"]

        data.to_csv(path_or_buf=self.path_to_file, sep=',', index=False)

        