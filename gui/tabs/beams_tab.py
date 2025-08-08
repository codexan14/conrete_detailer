import tkinter as tk
import tkinter.ttk as ttk
import core.beam_flexion_lrfd
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

    def update_path_to_file(self) -> None:
        self.path_to_file: str = self.path_to_folder.get() + "/beam_sections.csv"

    def calculate(self) -> None: 
        self.update_path_to_file() 
        data: pd.DataFrame = pd.read_csv(filepath_or_buffer=self.path_to_file, sep=',') #type: ignore

        positive_nominal_moment: list[float] = [0]*len(data["web_width"])
        negative_nominal_moment: list[float] = [0]*len(data["web_width"])
        flexural_reduction_factor: list[float] = [0]*len(data["web_width"])

        for web_width, height, concrete_compression_strength, top_reinforcement_area, top_reinforcement_centroid, bottom_reinforcement_area, bottom_reinforcement_centroid, i in zip(
            data["web_width"], 
            data["height"], 
            data["concrete_compression_strength"], 
            data["top_reinforcement_area"],
            data["top_reinforcement_centroid"],
            data["bottom_reinforcement_area"],
            data["bottom_reinforcement_centroid"],
            range(len(data["web_width"]))
        ):
            positive_nominal_moment[i] = core.beam_flexion_lrfd.calculate_positive_moment_capacity(
                web_width=web_width, 
                height=height, 
                concrete_compression_strength=concrete_compression_strength, 
                top_reinforcement_area = top_reinforcement_area, 
                top_reinforcement_centroid=top_reinforcement_centroid,
                bottom_reinforcement_area=bottom_reinforcement_area, 
                bottom_reinforcement_centroid=bottom_reinforcement_centroid, 
                steel_strain_max=0.0021)
            
            negative_nominal_moment[i] = core.beam_flexion_lrfd.calculate_negative_moment_capacity(
                web_width=web_width, 
                height=height, 
                concrete_compression_strength=concrete_compression_strength, 
                top_reinforcement_area = top_reinforcement_area, 
                top_reinforcement_centroid=top_reinforcement_centroid,
                bottom_reinforcement_area=bottom_reinforcement_area, 
                bottom_reinforcement_centroid=bottom_reinforcement_centroid, 
                steel_strain_max=0.0021)
            
            flexural_reduction_factor[i] = 0.90
        
        data["positive_nominal_moment"] = positive_nominal_moment
        data["negative_nominal_moment"] = negative_nominal_moment
        data["flexural_reduction_factor"] = flexural_reduction_factor
        data["positive_phi*Mn"] = data["positive_nominal_moment"] * data["flexural_reduction_factor"]
        data["negative_phi*Mn"] = data["negative_nominal_moment"] * data["flexural_reduction_factor"]

        data.to_csv(path_or_buf=self.path_to_file, sep=',', index=False)

        