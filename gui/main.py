from tkinter import *
from tkinter import ttk
from core.beam_flexion_lrfd import *
from gui.tabs.beams_tab import *

# Importing the modules
from gui.tabs.setting_tab import SettingModule
from gui.tabs.donation_tab import DonationModule
from gui.tabs.beams_tab import BeamModule


def beam_app(): 
    root = Tk() 
    root.geometry("400x400")
    root.title("Beam Designer")

    notebook = ttk.Notebook(master=root)
    notebook.grid(column=0, row=0, padx=25, pady=25)

    

    # Settings tab
    tab_01_container = SettingModule()
    notebook.add(child=tab_01_container.settings_tab, text="Settings")

    # Beams Tab
    tab_02_container = BeamModule(path_to_folder=tab_01_container.path_to_folder)
    notebook.add(child=tab_02_container.beams_tab, text="Beams")

    #Buy me a coffee!
    # DONATION_URL = ""

    # Donation tab
    tab_99_container = DonationModule()
    notebook.add(child=tab_99_container.donation_tab, text="Donation!")

    return root


if __name__ == '__main__':
    root = beam_app()
    root.mainloop()