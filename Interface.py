import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk


import numpy as np

class App(ttk.Frame):
    def __init__(self, parent, canvaSize):
        ttk.Frame.__init__(self)
        self.root = parent

        self.canvas = None
        self.canvaSize = canvaSize

        self.setupWidgets()

        # Widget variables
        toggleButtonVar = None


        # variable for drawing
        self.scale = 1
        self.offset = [self.canvaSize[0] / 2, self.canvaSize[1] / 2]
        self.layerNumber = 2

        self.colors = ['#cc0000', '#0000cc']

        # PCB variables
        self.VIASDATA = None
        self.TRACKSDATA = None

    def setupWidgets(self):
        # Set weight of columns and rows

        self.check_frame = ttk.LabelFrame(self, text="Graphic", width = 100, height=100)
        self.check_frame.grid(row=0, column=0, padx=10, pady=15, sticky="wnse")


        #Scrollbar
        self.scrollbar = ttk.Scrollbar(self.check_frame,orient = 'vertical')
        self.scrollbar.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="nswe")

        self.scrollbar2 = ttk.Scrollbar(self.check_frame, orient = 'horizontal')
        self.scrollbar2.grid(row=2, column=0, padx=(0, 0), pady=(0, 0), sticky="nswe")


        self.canvas = tk.Canvas(self.check_frame,height=600,width = 600, background="black", xscrollcommand=self.scrollbar2.set, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0,padx=(15,15),pady=(10,15), sticky="nsew")
        self.canvas.configure(scrollregion=(-600,-600,1200,1200))

        self.scrollbar.config(command=self.canvas.yview)
        self.scrollbar2.config(command=self.canvas.xview)

    def setupNotebook(self):
        self.toggleButtonVar = [ [tk.IntVar(), tk.IntVar(),tk.IntVar(), tk.IntVar()] for _ in range(self.layerNumber)]

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=1, padx=10, pady=15, sticky="nesw")

        ################################################################################################################
        # Tab 1
        self.tab_1 = ttk.Frame(self.notebook)
        self.tab_1.columnconfigure(index=0, weight=1)
        self.tab_1.columnconfigure(index=1, weight=1)
        self.tab_1.columnconfigure(index=2, weight=1)
        self.notebook.add(self.tab_1, text="Actions")

        for l in range(self.layerNumber):
            # Layer label
            self.label = ttk.Label(self.tab_1, text="Layer {}".format(l),justify="left",font=("-size", 12, "-weight", "bold"),)
            self.label.grid(row=l * 5, column=0, pady=5, columnspan=2)

            # Switch button for tracks
            switch = ttk.Checkbutton(self.tab_1, text="Tracks", style="Switch.TCheckbutton",
                                     variable = self.toggleButtonVar[l][0])
            switch.grid(row=l * 5 + 1, column=2, padx=0, pady=0, sticky="nsew")
            self.toggleButtonVar[l][0].set(1)

            # Switch button for objects
            switch = ttk.Checkbutton(self.tab_1, text="Objects", style="Switch.TCheckbutton",
                                     variable=self.toggleButtonVar[l][1])
            switch.grid(row=l * 5 + 2, column=2, padx=0, pady=0, sticky="nsew")
            self.toggleButtonVar[l][1].set(1)

            # Switch button for tracks
            switch = ttk.Checkbutton(self.tab_1, text="Copper areas", style="Switch.TCheckbutton",
                                     variable=self.toggleButtonVar[l][2])
            switch.grid(row=l * 5 + 3, column=2, padx=0, pady=0, sticky="nsew")
            self.toggleButtonVar[l][2].set(1)

            # Switch button for tracks
            switch = ttk.Checkbutton(self.tab_1, text="Power", style="Switch.TCheckbutton",
                                     variable=self.toggleButtonVar[l][3])
            switch.grid(row=l * 5 + 4, column=2, padx=0, pady=0, sticky="nsew")
            self.toggleButtonVar[l][3].set(1)

    # Custom drawing functions
    def drawVIA(self, VIASData):
        self.VIASDATA = VIASData
        for VIAData in VIASData:
            centerPos = [VIAData['CENTER_POSITION'][0] * self.scale + self.offset[0],
                         VIAData['CENTER_POSITION'][1] * self.scale + self.offset[0]]

            padSize = VIAData['PAD_RADIUS'] * self.scale
            holeSize = VIAData['HOLE_RADIUS'] * self.scale

            posExt = [centerPos[0] - padSize, centerPos[1] - padSize, centerPos[0] + padSize, centerPos[1] + padSize]
            posInt = [centerPos[0] - holeSize, centerPos[1] - holeSize, centerPos[0] + holeSize, centerPos[1] + holeSize]

            extCircle = self.canvas.create_oval(posExt[0], posExt[1], posExt[2], posExt[3], fill="#5c5c5c",
                                                    outline="#5c5c5c")
            intCircle = self.canvas.create_oval(posInt[0], posInt[1], posInt[2], posInt[3], fill="#262626",
                                                    outline="#262626")

    def drawTRACK(self, TRACKSData, selectLayer = 0,):
        self.TRACKSDATA = TRACKSData

        for TRACKData in TRACKSData:
            if selectLayer == 0:
                lineColor = self.colors[TRACKData['LAYER'] - 1]
                lineWidth = TRACKData['WIDTH'] * self.scale

                for id, _ in enumerate(TRACKData['POINT_LIST'][:-1]):
                    x0 = TRACKData['POINT_LIST'][id][0] * self.scale + self.offset[0]
                    y0 = TRACKData['POINT_LIST'][id][1] * self.scale + self.offset[1]
                    x1 = TRACKData['POINT_LIST'][id + 1][0] * self.scale + self.offset[0]
                    y1 = TRACKData['POINT_LIST'][id + 1][1] * self.scale + self.offset[1]

                    segment = self.canvas.create_line(x0, y0, x1, y1, fill=lineColor, width=lineWidth)
            else:
                if TRACKData['LAYER'] == selectLayer:

                    lineColor = self.colors[TRACKData['LAYER'] - 1]
                    lineWidth = TRACKData['WIDTH'] * self.scale

                    for id, _ in enumerate(TRACKData['POINT_LIST'][:-1]):
                        x0 = TRACKData['POINT_LIST'][id][0] * self.scale + self.offset[0]
                        y0 = TRACKData['POINT_LIST'][id][1] * self.scale + self.offset[1]
                        x1 = TRACKData['POINT_LIST'][id + 1][0] * self.scale + self.offset[0]
                        y1 = TRACKData['POINT_LIST'][id + 1][1] * self.scale + self.offset[1]

                        segment = self.canvas.create_line(x0, y0, x1, y1, fill=lineColor, width=lineWidth)



