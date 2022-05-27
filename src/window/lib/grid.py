import tkinter as tk

from src.window.lib.subGrid import subGrid

class mainGrid(tk.Frame):
    def __init__(self, parent):
        self.subGridList = []
        boxCoords = [element*parent.game.subgridSize for element in list(range(parent.game.subgridSize))]
        super().__init__(parent, bg='#181818', borderwidth=4, relief=tk.RAISED, height='698', width='698')
        self.grid_propagate(False)
        for gridY, boxY in enumerate(boxCoords):
            for gridX, boxX in enumerate(boxCoords):
                gridNbr = parent.game.boxNeighbours(boxY, boxX)
                markNbr = parent.game.pencilBoxNeighbours(boxY, boxX)
                tempItem = subGrid(self, gridNbr, markNbr, parent.game.subgridSize, parent.game.charSet)
                self.subGridList.append(tempItem)
                tempItem.grid(row=gridY, column=gridX, padx=1, pady=1)
    
    def update(self, game, solveHL=True):
        boxCoords = [element*game.subgridSize for element in list(range(game.subgridSize))]
        count = 0
        for boxY in boxCoords:
            for boxX in boxCoords:
                gridNbr = game.boxNeighbours(boxY, boxX)
                markNbr = game.pencilBoxNeighbours(boxY, boxX)
                self.subGridList[count].update(gridNbr, markNbr, solveHL)
                count += 1
    
    def updateNew(self, game):
        boxCoords = [element*game.subgridSize for element in list(range(game.subgridSize))]
        count = 0
        for boxY in boxCoords:
            for boxX in boxCoords:
                gridNbr = game.boxNeighbours(boxY, boxX)
                markNbr = game.pencilBoxNeighbours(boxY, boxX)
                self.subGridList[count].updateNew(gridNbr, markNbr)
                count += 1