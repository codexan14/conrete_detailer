from tkinter import *
from tkinter import ttk, filedialog
import tkinter.font as tkFont
from core.beam_lrfd import *
from typing import cast
from dataclasses import dataclass 
from pathlib import Path
import csv 

mainframe = Tk

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
        beam_file_header: list[str] = [
            "section_name",
            "base",
            "height",
            "concrete_strength",
            "rebar_area_top",
            "rebar_area_bottom",
            "rebar_position_top",
            "rebar_position_bottom",
            "steel_area_skin",
            "outter_stirrup_area",
            "inner_stirrups_area",
            "cover",
            "positive_nominal_moment",
            "negative_nominal_moment"]
        

        path = Path(self.path_to_folder.get() + "/beam_sections.csv")

        if not path.exists():
            path.touch()
            with open(file=path, mode='w') as file: 
                writer = csv.writer(file)
                writer.writerow(beam_file_header)
            Label(master=self.settings_tab, text="Project Created").grid(column=1, row=1)
        else: 
            Label(master=self.settings_tab, text="The file already exists").grid(column=1, row=1)
