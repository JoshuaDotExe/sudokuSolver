from pathlib import Path
import tkinter as tk

from src.window.lib.grid import mainGrid
from src.window.lib.logWidget import logWidget
from src.window.lib.debugWidget import debugWidget
from src.window.lib.inputGrid import inputGrid
from src.app.game import sudoku
from src import LOGDEBUG, __version__, LOGSOLVE



class mainWindow(tk.Tk):
    def __init__(self): #, gameObject: sudoku
        super().__init__()
        
        self.title(f'Sudoku Solver: {__version__}')
        iconPic = tk.PhotoImage(file=Path('src/resources/window/icon_32.png'))
        self.tk.call('wm','iconphoto', self._w, iconPic)
        self.resizable(True, True)
        self.state('zoomed')

        # Loads up a default grid of questionmarks
        self.game = sudoku.buildGridStr('?????????????????????????????????????????????????????????????????????????????????')
        
        self.mainGrid = mainGrid(self)
        self.mainGrid.grid(row=0, column=0, columnspan=3, rowspan=3, padx=10, pady=10)
        
        self.logWidgetContainer = tk.LabelFrame(self, text='Solution Log')
        self.logWidget = logWidget(self.logWidgetContainer, self)
        self.logWidget.pack(fill='both', padx=5, pady=5)
        self.logWidgetContainer.grid(row=3, column=0, columnspan=3, pady=5, padx=5)
        
        self.debugWidgetContainer = tk.LabelFrame(self, text='Debug Log')
        self.debugWidget = debugWidget(self.debugWidgetContainer, self)
        self.debugWidget.pack(fill='both', padx=5, pady=5)
        self.debugWidgetContainer.grid(row=2, column=4, rowspan=2, pady=5, padx=5)
        
        self.commandFrame = tk.LabelFrame(self, text='Commands')
        
        self.solveButtonsContainer = tk.LabelFrame(self.commandFrame, text='Solving')
        self.fullSolveButton = tk.Button(self.solveButtonsContainer, text='Solve Full', command=self.runFull, state='disabled')
        self.fullSolveButton.grid(row=0, pady=10, padx=10)
        self.partSolveButton = tk.Button(self.solveButtonsContainer, text='Solve Once', command=self.runOnce, state='disabled')
        self.partSolveButton.grid(row=1, pady=10, padx=10)
        self.solveButtonsContainer.grid(row=0, column=0, pady=10, padx=10)
        
        self.inputFrame = tk.LabelFrame(self.commandFrame, text='Input')
        self.gridInputButton = tk.Button(self.inputFrame, text='Input Grid', command=self.runGridInput)
        self.gridInputButton.grid(row=0, column=0, padx=10, pady=10)
        exampleGame = '7..3.9..1....5....82..6.....59.....36.2...1.93.....65.....7..94....8....9..1.3..7'
        self.gameStrInput = tk.Entry(self.inputFrame, width=51, font=('Arial', '12'))
        self.gameStrInput.insert(tk.END, exampleGame)
        self.gameStrInput.grid(row=1, column=0, pady=10, padx=10)
        self.inputStrButton = tk.Button(self.inputFrame, text='Input Str', command=self.insertNewGame)
        self.inputStrButton.grid(row=1, column=1, pady=10, padx=10)
        self.inputFrame.grid(row=0, column=1, pady=10, padx=10)
        
        self.commandFrame.grid(column=4, row=0)
        
    @staticmethod
    def disableButtons(buttons: list):
        for button in buttons:
            button['state'] = 'disable'
    
    @staticmethod
    def enableButtons(buttons: list):
        for button in buttons:
            button['state'] = 'active'
    
    @staticmethod
    def enableTextBoxes(boxes: list):
        for box in boxes:
            box.configure(state='normal')
    
    @staticmethod
    def disableTextBoxes(boxes: list):
        for box in boxes:
            box.configure(state='disabled')
    
    def runGridInput(self):
        gridWindow = inputGrid(self)
    
    def runFull(self):
        self.disableButtons([self.fullSolveButton, self.partSolveButton])
        self.game.solveFull()
        self.mainGrid.update(self.game, solveHL=False)
    
    def runOnce(self):
        self.disableButtons([self.fullSolveButton, self.partSolveButton])
        returnVal = self.game.solveOnce()
        # Keeps the buttons disabled if the sudoku has been solved
        if returnVal == True: 
            self.mainGrid.update(self.game, solveHL=False)
            return
        self.mainGrid.update(self.game)
        self.enableButtons([self.fullSolveButton, self.partSolveButton])
        
    def insertNewGame(self):
        grabbedStr = self.gameStrInput.get()
        if len(grabbedStr) != 81:
            LOGDEBUG.warning('String input length unsupported')
            return
        self.game = sudoku.buildGridStr(grabbedStr)
        self.enableButtons([self.fullSolveButton, self.partSolveButton])
        self.mainGrid.updateNew(self.game)
        self.enableTextBoxes([self.logWidget, self.debugWidget])
        self.logWidget.delete(1.0, tk.END)
        self.debugWidget.delete(1.0, tk.END)
        self.disableTextBoxes([self.logWidget, self.debugWidget])