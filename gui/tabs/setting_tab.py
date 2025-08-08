from tkinter import * # type: ignore
from tkinter import ttk, filedialog
from core.beam_flexion_lrfd import *
from pathlib import Path
import csv 

class SettingModule:
    def __init__(self) -> None: 
        self.settings_tab = ttk.Frame()
        self.path_to_folder = StringVar(master=None, value=".")
        Label(master=self.settings_tab, textvariable=self.path_to_folder).grid(column=1, row=0)

        Button(master=self.settings_tab, text="Select Folder", command=self.get_folder).grid(column=0, row=0)
        Button(master=self.settings_tab, text="Create Project", command=self.create_project).grid(column=0, row=1)

    def get_folder(self) -> None: 
        self.path_to_folder.set(filedialog.askdirectory(
            title="Select Folder",
            initialdir= self.path_to_folder.get()       # Always takes the current directory
        ))

    def create_project(self) -> None: 
        self.beam_file_header: list[str] = [
            "section_name",
            "web_width",
            "height",
            "concrete_compression_strength",
            "top_reinforcement_area",
            "bottom_reinforcement_area",
            "top_reinforcement_centroid",
            "bottom_reinforcement_centroid",
            "skin_reinforcement_area",
            "outter_stirrup_area",
            "inner_stirrups_area",
            "cover",
            "positive_nominal_moment",
            "negative_nominal_moment",
            "flexural_reduction_factor", 
            "shear_reduction_factor",
            "ultimate_positive_moment_limit",
            "ultimate_negative_moment_limit",
            "ultimate_shear_strength"]
        
        path = Path(self.path_to_folder.get() + "/beam_sections.csv")

        if not path.exists():
            path.touch()
            with open(file=path, mode='w') as file: 
                writer = csv.writer(file)
                writer.writerow(self.beam_file_header)
            Label(master=self.settings_tab, text="Project Created").grid(column=1, row=1)
        else: 
            Label(master=self.settings_tab, text="The file already exists").grid(column=1, row=1)
