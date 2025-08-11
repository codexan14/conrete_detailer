from tkinter import * # type: ignore
from tkinter import ttk

from PIL.ImageFile import ImageFile
from core.beam_flexion_lrfd import *
from PIL import Image, ImageTk
import webbrowser
from typing import cast

import sys
import os

def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundle runtime folder
        base_path: str = cast(str,sys._MEIPASS)
    else:
        # Running normally (dev)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DonationModule:
    def __init__(self) -> None: 
        self.donation_tab = ttk.Frame()
        image: Image.Image = Image.open(resource_path("gui/img/yellow-button.png")).resize((200, 60), Image.Resampling.LANCZOS)
        self.coffee_img: ImageTk.PhotoImage = ImageTk.PhotoImage(image=image, size=(50,50))
        
        Button(master=self.donation_tab, image=self.coffee_img, command=self.open_donation).grid(column=0, row=0)
        Label(master=self.donation_tab, text="Please support the development of this software").grid(column=0, row=1)
    
    def open_donation(self) -> None: 
        DONATION_URL: str = r"https://buymeacoffee.com/codex.an14"
        webbrowser.open_new_tab(DONATION_URL)