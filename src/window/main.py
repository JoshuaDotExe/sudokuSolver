import tkinter as tk
import logging

from src.window.lib.grid import mainGrid
from src.window.lib.logWidget import logWidget
from src.app.game import sudoku
from src import __version__

def startUp():
    print(f"Running Sudoku Solver : Version # {__version__}")
    logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.FileHandler("logging/debug.log"),
                              logging.StreamHandler()])
    return True

class mainWindow(tk.Tk):
    def __init__(self): #, gameObject: sudoku
        super().__init__()
        
        self.title(f'Sudoku Solver: {__version__}')
        self.iconbitmap('src/resources/window/icon_32.ico')
        self.resizable(True, True)
        
        self.game = sudoku.buildGridStr('7..3.9..1....5....82..6.....59.....36.2...1.93.....65.....7..94....8....9..1.3..7')
        
        titleContainer = tk.Frame(self, bg='#c4f5d1')
        tk.Label(titleContainer, text='This is a title').pack(pady=20, padx=20)
        titleContainer.grid(row=0, column=1)
        
        mainGrid(self).grid(row=1, column=0, columnspan=3, rowspan=3, padx=10)
        logWidget(tk.Frame(self)).container.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
        
        tk.Button(self, text='Solve', command=self.runPuzzle).grid(row=0, column=2)
        


    def runPuzzle(self):
        while self.game.solved == False:
            self.game.methods()
            if self.game.turnMoves == 0:
                self.game.solved = True
                logging.warning("Game Currently Unsolvable")
                print(self.game)
                return
            if self.game.solvedCheck() == True:
                self.game.solved = True
                logging.info("Game Solved")
                print(self.game)

def main():
    app = mainWindow()
    app.mainloop()
    
if __name__ == "__main__":
    main()

