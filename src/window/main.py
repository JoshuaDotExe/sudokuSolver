from os import stat
import tkinter as tk
import logging

from src.window.lib.grid import mainGrid
from src.window.lib.logWidget import logWidget
from src.window.lib.debugWidget import debugWidget
from src.app.game import sudoku
from src import LOGDEBUG, __version__, LOGSOLVE



class mainWindow(tk.Tk):
    def __init__(self): #, gameObject: sudoku
        super().__init__()
        
        self.title(f'Sudoku Solver: {__version__}')
        self.iconbitmap('src/resources/window/icon_32.ico')
        self.resizable(True, True)
        self.state('zoomed')
        # 94..2..38...418..............7.8.5...6.1.3.4...5.6.2..............231...21..4..96
        # 7..3.9..1....5....82..6.....59.....36.2...1.93.....65.....7..94....8....9..1.3..7
        # ?????????????????????????????????????????????????????????????????????????????????
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
        self.debugWidgetContainer.grid(row=2, column=4, rowspan=10, pady=5, padx=5)
        
        self.fullSolveButton = tk.Button(self, text='Solve Full', command=self.runFull)
        self.fullSolveButton.grid(row=0, column=4)
        self.partSolveButton = tk.Button(self, text='Solve Once', command=self.runOnce)
        self.partSolveButton.grid(row=1, column=4)
        
    def runFull(self):
        self.fullSolveButton['state'] = 'disabled'
        LOGSOLVE.info('Running methods to completion...')
        while self.game.solved == False:
            self.game.methods()
            if self.game.turnMoves == 0:
                self.game.solved = True
                LOGSOLVE.warning("Game Currently Unsolvable")
                print(self.game)
            elif self.game.solvedCheck() == True:
                self.game.solved = True
                LOGSOLVE.info("Game Solved")
                print(self.game)
        self.mainGrid.update(self.game)
        if self.game.solved == True:
            self.disableButtons([self.fullSolveButton, self.partSolveButton])
            return
        self.fullSolveButton['state'] = 'active'
    
    @staticmethod
    def disableButtons(buttons: list):
        for button in buttons:
            button['state'] = 'disable'
    
    @staticmethod
    def enableButtons(buttons: list):
        for button in buttons:
            button['state'] = 'active'
    
    def runOnce(self):
        self.partSolveButton['state'] = 'disabled'
        LOGSOLVE.info('Running single method...')
        self.game.methods()
        if self.game.turnMoves == 0:
            self.game.solved = True
            LOGSOLVE.warning("Game Currently Unsolvable")
            LOGDEBUG.warning('Required method not available')
            self.mainGrid.update(self.game)
            self.disableButtons([self.fullSolveButton, self.partSolveButton])
            return
        elif self.game.solvedCheck() == True:
            self.game.solved = True
            LOGSOLVE.info("Game Solved")
            self.mainGrid.update(self.game)
            self.disableButtons([self.fullSolveButton, self.partSolveButton])
            return
        self.mainGrid.update(self.game)
        self.partSolveButton['state'] = 'active'

def main():
    print(f"Running Sudoku Solver : Version # {__version__}")
    logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.FileHandler("logging/debug.log"),
                              logging.StreamHandler()])
    app = mainWindow()
    app.mainloop()
    
if __name__ == "__main__":
    main()

