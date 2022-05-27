import tkinter as tk

from src.app.game import sudoku
from src import LOGDEBUG

class inputGrid(tk.Toplevel):
    def __init__(self, parent):
        parent.disableButtons([parent.gridInputButton, parent.inputStrButton])
        self.gridStr = ''
        self.entryArray = []
        super().__init__()
        self.title('Grid Input')
        closeL = lambda parent=parent: self.on_close(parent)
        self.protocol('WM_DELETE_WINDOW', closeL)
        self.gridFrame = tk.Frame(self, bg='gray')
        
        # Lambda validation for the entry widget to only allow a single digit input
        validL = lambda txt : True if len(txt) == 0 or (len(txt) <= 1 and txt in parent.game.charSet) else False
        validFunc = (self.register(validL), '%P')
        
        for y in range(9):
            tempList = []
            for x in range(9):
                tempFrame = tk.Frame(self.gridFrame, width=50, height=50)
                tempFrame.pack_propagate(False)
                tempEntry = tk.Entry(tempFrame, font=("fixed", "30"), justify='center', validate='key', validatecommand=validFunc)
                tempEntry.pack(fill='both')
                tempFrame.grid(row=y, column=x)
                tempList.append(tempEntry)
            self.entryArray.append(tempList)
        self.gridFrame.grid(row=0, column=0, rowspan=5, columnspan=5, padx=10, pady=10)
        
        submitL = lambda parent=parent: self.submit(parent)
        cancelL = lambda parent=parent: self.cancel(parent)
        self.submitButton = tk.Button(self, text='SUBMIT', command=submitL)
        self.submitButton.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.cancelButton = tk.Button(self, text='CANCEL', command=cancelL)
        self.cancelButton.grid(row=5, column=3, columnspan=2, padx=10, pady=10)
    
    def on_close(self, parent):
        parent.enableButtons([parent.gridInputButton, parent.inputStrButton])
        self.destroy()
    
    def getStr(self):
        returnStr = ''
        for row in self.entryArray:
            for item in row:
                itemStr = item.get()
                if len(itemStr) == 0:
                    returnStr += '.'
                    continue
                returnStr += itemStr
        return returnStr
    
    def submit(self, parent):
        # Insert valid game check here
        # if True:
        #     pass
        parent.game = sudoku.buildGridStr(self.getStr())
        parent.enableButtons([parent.fullSolveButton, parent.partSolveButton])
        parent.mainGrid.updateNew(parent.game)
        parent.enableTextBoxes([parent.logWidget, parent.debugWidget])
        parent.logWidget.delete(1.0, tk.END)
        parent.debugWidget.delete(1.0, tk.END)
        parent.disableTextBoxes([parent.logWidget, parent.debugWidget])
        parent.enableButtons([parent.gridInputButton, parent.inputStrButton])
        self.destroy()
        
    
    def cancel(self, parent):
        parent.enableButtons([parent.gridInputButton, parent.inputStrButton])
        self.destroy()