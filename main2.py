import json
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk

from Interface import *

from jsonParser import parserJSONFile

CANVAS_SIZE = [600,600]

LAYER_NUMBER = 2


# Screen update variables
TB_var = [ [1,1,1,1] for _ in range(LAYER_NUMBER)]
scale = 1

forceUpdate = False

def checkEvents(root, interface):
    global scale, forceUpdate
    # Check button in the interface
    isChanged = False
    for lId,layer in enumerate(interface.toggleButtonVar):
        for vId,var in enumerate(layer):
            if (TB_var[lId][vId] != var.get()):
                isChanged = True
                TB_var[lId][vId] = var.get()

    if isChanged or forceUpdate:
        app.scale = scale
        interface.canvas.delete("all")
        interface.drawVIA(interface.VIASDATA)
        for lId, layer in enumerate(TB_var):
            if layer[0] == 1:
                # track var
                interface.drawTRACK(interface.TRACKSDATA, selectLayer=(lId + 1))

        forceUpdate = False


    root.after(100, lambda: checkEvents(root, interface))  # reschedule event in 2 seconds

def mouse_wheel(event):
    global scale, forceUpdate
    # respond to Linux or Windows wheel event
    if event.num == 5 or event.delta == -120:
        scale -= 0.1
    if event.num == 4 or event.delta == 120:
        scale += 0.1

    forceUpdate = True

if __name__ == '__main__':
    root = tk.Tk()
    root.title("PCB Power Analyzer")

    # Set the theme for the window - obv dark theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    #
    app = App(root, CANVAS_SIZE)
    app.pack(fill="both", expand=True)

    #Bind buttons
    root.bind("<MouseWheel>", mouse_wheel)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

    # Start looping functions
    root.after(100, lambda: checkEvents(root, app))  # reschedule event in 2 seconds

    ###############################################################################################
    PCBElements = parserJSONFile("LedBoard.json")

    app.drawVIA(PCBElements['VIAS'])
    app.drawTRACK(PCBElements['TRACKS'])

    ###############################################################################################


    app.setupNotebook()

    root.mainloop()

