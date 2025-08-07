from tkinter import *
from tkinter import ttk, filedialog
import tkinter.font as tkFont
from core.beam_lrfd import *

root = Tk() 
root.geometry("400x400")
root.title("Beam Designer")

notebook = ttk.Notebook(root)
notebook.grid(column=0, row=0, padx=25, pady=25)


# Settings tab
from gui.tabs.setting_tab import SettingModule
tab_1_container = SettingModule()
notebook.add(tab_1_container.settings_tab, text="Settings")

# Beams Tab
from gui.tabs.beams_tab import BeamModule
tab_2_container = BeamModule(path_to_folder=tab_1_container.path_to_folder)
notebook.add(tab_2_container.beams_tab, text="Beams")


# normal_font = tkFont.Font(family="Arial", size = 12)
# subheader_font = tkFont.Font(family="Arial", size = 17)
# header_font = tkFont.Font(family="Arial", size = 24)


# # SELECTS THE FOLDER
# def select_folder(): 
#     folder_path = filedialog.askdirectory(
#         title="Select Folder",
#         initialdir="/"
#     )

#     if folder_path: 
#         folder_var.set(folder_path)
#         status_label.config(text=f"Selected folder: {folder_path}")
    
# #Variable to store folder path
# folder_var = StringVar()
# status_label = ttk.Label(mainframe, text="No folder selected")
# # INPUTS
# ttk.Label(mainframe, text="Inputs", font=subheader_font).grid(column=0, row=0, padx=10, pady=10, columnspan=3, sticky=(W))

# ttk.Label(mainframe, width=7, text="Base", font = normal_font).grid(column=0, row=1, sticky=(W))
# base = StringVar()
# base_widget = ttk.Entry(mainframe, width=7, textvariable=base)
# base_widget.grid(column=1, row=1, padx=10, pady=10)
# ttk.Label(mainframe, width=7, text="mm", font = normal_font).grid(column=2, row=1, sticky=(W, E))

# ttk.Label(mainframe, width=7, text="Height", font = normal_font).grid(column=0, row=2, sticky=(W, E))
# height = StringVar()
# height_widget = ttk.Entry(mainframe, width=7, textvariable=height)
# height_widget.grid(column=1, row=2, padx=10, pady=10)
# ttk.Label(mainframe, width=7, text="mm", font = normal_font).grid(column=2, row=2, sticky=(W, E))

# # OUTPUTS! 
# ttk.Label(mainframe, width=6, text="Outputs", font=subheader_font).grid(column=3, row=0)
# area = StringVar()
# ttk.Label(mainframe, textvariable=area, font=normal_font).grid(column=3, row=1)


# def on_click() -> None: 
#     area.set(calculate_beam_maximum_bottom_reinforcement(
#         base=float(base.get()),
#         rebar_area_top=0,
#         rebar_position_bottom=530,
#         rebar_position_top=70,
#         concrete_strength=28,
#         steel_yield_stress=420
#     ))

#     Toplevel(mainframe)

# Button_1: None = ttk.Button(mainframe, width=7, text="Submit", command=on_click).grid(column=0, row=100, columnspan=3)
# Button_2: None = ttk.Button(mainframe, width=7, text="Select Folder", command=select_folder).grid(column=0, row=101, columnspan=3)



if __name__ == '__main__':
    root.mainloop()
