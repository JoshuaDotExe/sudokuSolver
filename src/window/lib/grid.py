import tkinter as tk

from src.window.lib.subGrid import subGrid

class mainGrid(tk.Frame):
    def __init__(self, parent):
        boxCoords = [element*parent.game.subgridSize for element in list(range(parent.game.subgridSize))]
        super().__init__(parent, bg='#181818', borderwidth=4, relief=tk.RAISED)
        for gridY, boxY in enumerate(boxCoords):
            for gridX, boxX in enumerate(boxCoords):
                gridNbr = parent.game.boxNeighbours(boxY, boxX)
                markNbr = parent.game.pencilBoxNeighbours(boxY, boxX)
                subGrid(self, gridNbr, markNbr, parent.game.subgridSize, parent.game.charSet).grid(row=gridY, column=gridX, padx=1, pady=1)
        