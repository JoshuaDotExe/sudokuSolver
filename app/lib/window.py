import tkinter as tk
from os import getcwd
from tkinter import font

from app import __version__
from app.lib.sudoku import sudoku

cwd = getcwd().replace("\\", "/")

root = tk.Tk()

root.title(f'Sudoku solver | Version {__version__}')
root.iconbitmap(cwd + '/app/resources/window/icon_32.ico')
root.geometry('700x700')

class mainWindow:
    
    def __init__(self, master):
        gridFrame = tk.Frame(master, borderwidth=1, relief=tk.SUNKEN)
        gridFrame.grid(row=0, column=0, 
                       padx=10, pady=10,
                       rowspan=3, columnspan=3)
        
        infoFrame = tk.Frame(master)
        infoFrame.grid(row=0, column=3)
        
        statFrame = tk.Frame(infoFrame, )
        statFrame.pack()
        
        self.game = sudoku.loadFromJSON('simple')

        self.gridDisplay(gridFrame)
        self.statDisplay(statFrame)
        
    def gridDisplay(self, frame: tk.Frame):
        subGridNum = self.game.subgridSize
        for boxY in range(subGridNum):
            for boxX in range(subGridNum):
                boxFrame = tk.Frame(frame, bd=4)
                boxFrame.grid(row=boxY, column=boxX)
                for num, element in enumerate(self.game.boxNeighbours(subGridNum*boxY, subGridNum*boxX)):
                    xCoord = num%subGridNum
                    yCoord = num//subGridNum
                    elementFrame = tk.Frame(boxFrame, bd=2, relief=tk.RAISED,
                                            height=70, width=70)
                    elementFrame.pack_propagate(False)
                    elementFrame.grid_propagate(False)
                    elementFrame.grid(row=yCoord, column=xCoord)
                    if element == '0':
                        self.gridDisplayEmpty(elementFrame, 
                                            self.game.pencilMarks[(subGridNum*boxY)+yCoord][(subGridNum*boxX)+xCoord])
                    else:
                        self.gridDisplayOccup(elementFrame, element)
                
                    
    def gridDisplayEmpty(self, frame: tk.Frame, elements: list):
        for num, item in enumerate(self.game.charSet):
            if item not in elements:
                item = ' '
            xCoord = num%self.game.subgridSize
            yCoord = num//self.game.subgridSize
            tk.Label(frame, text=f' {item} ',
                    font=('Ariel',10)
                    ).grid(row=yCoord, column=xCoord, padx=0, pady=0)
    def gridDisplayOccup(self, frame: tk.Frame, element: str):
        tk.Label(frame, text=element,
                 font=('Helvetica',40)
                 ).pack()
    
    def statDisplay(self, frame: tk.Frame):
        turnLabel = tk.Label(frame, text=f"Turn # : {self.game.turnCounter}")
        difLabel = tk.Label(frame, text=f"Difficulty (1-10) : {self.game.difficulty if self.game.difficulty != 0 else '?'}")
        solvedLabel = tk.Label(frame, text=f"Solved : {self.game.solved}")
        
        turnLabel.pack()
        difLabel.pack()
        solvedLabel.pack()
        #turnLabel.grid(row=0, column=0)
        #difLabel.grid(row=1, column=0)
        
mainWin = mainWindow(root)

root.mainloop()