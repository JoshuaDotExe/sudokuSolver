import tkinter as tk

from src import LOGDEBUG

class subGrid(tk.Frame):
    def __init__(self, container, gridBox, markBox, SQRT, charSet):
        super().__init__(container, bg='#C0C0C0')
        self.gridCheck = gridBox
        self.charSet = charSet
        self.SQRT = SQRT
        self.labelList = []
        self.initWhitelist = []
        for itemIndex, item in enumerate(gridBox):
            x = (itemIndex%SQRT) * SQRT
            y = (itemIndex//SQRT) * SQRT
            if item != '0':
                tempLabel = tk.Label(self, text=item, fg='blue', width=4, height=2, font=("Helvetica", "20"))
                tempLabel.grid(row=y, column=x, rowspan=SQRT, columnspan=SQRT, padx=1, pady=1)
                self.labelList.append(tempLabel)
                self.initWhitelist.append(itemIndex)
                continue
            textStr = self.buildMarkLabelStr(markBox[itemIndex])
            tempLabel = tk.Label(self, text=textStr, width=8, height=4, font=("courier", "10"))
            tempLabel.grid_propagate(False)
            self.labelList.append(tempLabel)
            tempLabel.grid(row=y, column=x, rowspan=SQRT, columnspan=SQRT, padx=1, pady=1)
    
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
                continue
            if newGrid != oldGrid:
                colour = 'red' if solveHL == True else 'black'
                self.labelList[itemIndex].config(text=newGrid, font=("Helvetica", "20"), fg=colour, width=4, height=2)
                continue
            if self.labelList[itemIndex].cget("fg") == 'red': 
                self.labelList[itemIndex].config(fg='black')
        self.gridCheck = gridBox
    
    def updateNew(self, gridBox, markBox):
        self.gridCheck = gridBox
        self.markCheck = markBox
        for itemIndex, newGrid in enumerate(gridBox):
            if newGrid != '0':
                self.labelList[itemIndex].config(text=newGrid, font=("Helvetica", "20"), fg='blue', width=4, height=2)
                continue
            self.labelList[itemIndex].config(fg='black', text=self.buildMarkLabelStr(markBox[itemIndex]), width=8, height=4, font=("courier", "10"))
            