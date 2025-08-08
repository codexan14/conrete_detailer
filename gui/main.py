from tkinter import *
from tkinter import ttk
from core.beam_flexion_lrfd import *
import webbrowser

root = Tk() 
root.geometry("400x400")
root.title("Beam Designer")

notebook = ttk.Notebook(root)
notebook.grid(column=0, row=0, padx=25, pady=25)

#Buy me a coffee!
DONATION_URL = ""

# Donation tab
from gui.tabs.donation_tab import DonationModule
tab_0_container = DonationModule()
notebook.add(tab_0_container.donation_tab, text="Donation!")

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
