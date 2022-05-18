import logging
import time
from copy import deepcopy

from src.app.game import sudoku

from src import __version__
from src.app import textLogo



def startUp():
    print(f"Running Sudoku Solver : Version # {__version__}")
    logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.FileHandler("debug.log"),
                              logging.StreamHandler()])
    logging.basicConfig(level=logging.INFO,
                        handler=[logging.FileHandler("debug.log"),
                                logging.StreamHandler()])
    logging.basicConfig(level=logging.WARNING,
                        handler=[logging.FileHandler("debug.log"),
                                logging.StreamHandler()])
    logging.basicConfig(level=logging.CRITICAL,
                        handler=[logging.FileHandler("debug.log"),
                                logging.StreamHandler()])
    return True

def runPuzzle(puzzle: sudoku):
    print(textLogo)
    
    while puzzle.solved == False:
        print(puzzle)
        input()
        puzzle.methods()
        if puzzle.turnMoves == 0:
            puzzle.solved = True
            logging.warning("Game Currently Unsolvable")
            print(puzzle)
            return
        if puzzle.solvedCheck() == True:
            puzzle.solved = True
            logging.info("Game Solved")
            print(puzzle)

# Continuously runs puzzles for a set length of runTime and prints counter and time
def runTimedPuzzle(puzzle: sudoku):
    print(textLogo)
    input("Enter to start")
    startTime = time.time()
    counter = 0
    runTime = 1
    while time.time()-startTime < runTime:
        counter += 1
        cPuzzle = deepcopy(puzzle)
        while cPuzzle.solved == False:
            cPuzzle.methods()
            if cPuzzle.solvedCheck() == True:
                cPuzzle.solved = True
                logging.info("Game Solved")
            
    print(f'Games Finished = {counter}\nFinished in {(time.time()-startTime)} seconds')
def main():
    startUp()
    gameItem = sudoku.buildGridStr(input('Please enter a game string : '))
    runPuzzle(gameItem)
    #runTimedPuzzle(gameItem)
    #94..2..38...418..............7.8.5...6.1.3.4...5.6.2..............231...21..4..96