from tkinter import *
from tkinter import ttk, filedialog
import tkinter.font as tkFont
from core.beam_flexion_lrfd import *

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

if __name__ == '__main__':
    root.mainloop()
