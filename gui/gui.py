from tkinter import *
from tkinter import ttk 
import tkinter.font as tkFont
from core.beam_lrfd import *
from typing import cast



root = Tk() 
root.geometry("400x400")
root.title("Beam Designer")

normal_font = tkFont.Font(family="Arial", size = 12)
subheader_font = tkFont.Font(family="Arial", size = 17)
header_font = tkFont.Font(family="Arial", size = 24)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, padx=25, pady=25, sticky=(N, W, E, S))

# INPUTS
ttk.Label(mainframe, text="Inputs", font=subheader_font).grid(column=0, row=0, padx=10, pady=10, columnspan=3, sticky=(W))

ttk.Label(mainframe, width=7, text="Base", font = normal_font).grid(column=0, row=1, sticky=(W))
base = StringVar()
base_widget = ttk.Entry(mainframe, width=7, textvariable=base)
base_widget.grid(column=1, row=1, padx=10, pady=10)
ttk.Label(mainframe, width=7, text="mm", font = normal_font).grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, width=7, text="Height", font = normal_font).grid(column=0, row=2, sticky=(W, E))
height = StringVar()
height_widget = ttk.Entry(mainframe, width=7, textvariable=height)
height_widget.grid(column=1, row=2, padx=10, pady=10)
ttk.Label(mainframe, width=7, text="mm", font = normal_font).grid(column=2, row=2, sticky=(W, E))

# OUTPUTS! 
ttk.Label(mainframe, width=6, text="Outputs", font=subheader_font).grid(column=3, row=0)
area = StringVar()
ttk.Label(mainframe, textvariable=area, font=normal_font).grid(column=3, row=1)


def on_click() -> None: 
    area.set(calculate_beam_maximum_bottom_reinforcement(
        base=float(base.get()),
        rebar_area_top=0,
        rebar_position_bottom=530,
        rebar_position_top=70,
        concrete_strength=28,
        steel_yield_stress=420
    ))

Button = ttk.Button(mainframe, width=7, text="Submit", command=on_click).grid(column=0, row=100, columnspan=3)



if __name__ == '__main__':
    root.mainloop()
