from tkinter import * # type: ignore
from tkinter import ttk

from PIL.ImageFile import ImageFile
from core.beam_flexion_lrfd import *
from PIL import Image, ImageTk
import webbrowser

class DonationModule:
    def __init__(self) -> None: 
        self.donation_tab = ttk.Frame()
        image: Image.Image = Image.open("gui/img/yellow-button.png").resize((200, 60), Image.Resampling.LANCZOS)
        self.coffee_img: ImageTk.PhotoImage = ImageTk.PhotoImage(image=image, size=(50,50))
        
        Button(master=self.donation_tab, image=self.coffee_img, command=self.open_donation).grid(column=0, row=0)
        Label(master=self.donation_tab, text="Please support the development of this software").grid(column=0, row=1)
    
    def open_donation(self) -> None: 
        DONATION_URL: str = r"https://buymeacoffee.com/codex.an14"
        webbrowser.open_new_tab(DONATION_URL)