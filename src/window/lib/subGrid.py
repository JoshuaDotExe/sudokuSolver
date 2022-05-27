from distutils.debug import DEBUG
from tarfile import PAX_FIELDS
import tkinter as tk

from src import LOGDEBUG

class subGrid(tk.Frame):
    def __init__(self, container, gridBox, markBox, SQRT, charSet):
        super().__init__(container, bg='#C0C0C0', width=228, height=228)
        self.grid_propagate(False)
        self.gridCheck = gridBox
        self.charSet = charSet
        self.SQRT = SQRT
        self.LFont = ("fixed", "26")
        self.SFont = ("fixed", "10")
        self.labelList = []
        self.initWhitelist = []
        for itemIndex, item in enumerate(gridBox):
            x = itemIndex%SQRT
            y = itemIndex//SQRT
            labelContainer = tk.Frame(self, width=74, height=74)
            labelContainer.pack_propagate(False)
            if item != '0':
                tempLabel = tk.Label(labelContainer, text=item, fg='blue', font=self.LFont)
                #self.updatePadding(tempLabel)
                tempLabel.pack(fill='both', pady=(15, 0))
                labelContainer.grid(row=y, column=x, padx=1, pady=1)
                self.labelList.append(tempLabel)
                self.initWhitelist.append(itemIndex)
                continue
            textStr = self.buildMarkLabelStr(markBox[itemIndex])
            tempLabel = tk.Label(labelContainer, text=textStr, font=self.SFont)
            #self.updatePadding(tempLabel)
            tempLabel.pack(fill='both')
            self.labelList.append(tempLabel)
    
    def buildMarkLabelStr(self, targetMarks):
        finStr = str()
        for charIndex, char in enumerate(self.charSet):
            finStr += f'{char}' if char in targetMarks else ' '
            finStr += '\n' if charIndex%self.SQRT == 2 else ' '
        finStr += ' '
        return finStr[:-2]
    
    def update(self, gridBox, markBox, solveHL):
        for itemIndex ,(newGrid, oldGrid) in enumerate(zip(gridBox, self.gridCheck)):
            if newGrid == '0':
                self.labelList[itemIndex].config(text=self.buildMarkLabelStr(markBox[itemIndex]))
                #self.updatePadding(self.labelList[itemIndex])
                continue
            if newGrid != oldGrid:
                colour = 'red' if solveHL == True else 'black'
                self.labelList[itemIndex].config(text=newGrid, font=self.LFont, fg=colour)
                #self.updatePadding(self.labelList[itemIndex])
                continue
            if self.labelList[itemIndex].cget("fg") == 'red': 
                self.labelList[itemIndex].config(fg='black')
        self.gridCheck = gridBox
    
    def updateNew(self, gridBox, markBox):
        self.gridCheck = gridBox
        self.markCheck = markBox
        for itemIndex, newGrid in enumerate(gridBox):
            if newGrid != '0':
                self.labelList[itemIndex].config(text=newGrid, font=self.LFont, fg='blue')
                #self.updatePadding(self.labelList[itemIndex])
                continue
            self.labelList[itemIndex].config(fg='black', text=self.buildMarkLabelStr(markBox[itemIndex]), font=self.SFont)
            #self.updatePadding(self.labelList[itemIndex])
            
            