import socket
import sys
from tkinter import Tk

def single_instance(port: int=65432) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error:
        print("Another instance is already running.")
        sys.exit(0)
    return s  # Keep socket alive

if __name__ == "__main__":
    sock: socket.socket = single_instance()

    from gui.main import beam_app

    root: Tk = beam_app()
    root.mainloop()




# pyinstaller --noconsole --onefile gui/main.py --add-data "gui/img;gui/img" --add-data "core;core" --add-data "gui/tabs;gui/tabs" --hidden-import numpy --hidden-import pandas --hidden-import tkinter.filedialog --hidden-import PIL --hidden-import PIL.ImageFile  
