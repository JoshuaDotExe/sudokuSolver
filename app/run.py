import logging
import time
from copy import deepcopy

from app.sudoku.game import sudoku

from app import __version__
from app.sudoku import textLogo



def startUp():
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
    print(f"Running Sudoku Solver : Version # {__version__}")
    
    return True
def runPuzzle(puzzle: sudoku):
    print(textLogo)
    print(puzzle)
    while puzzle.solved == False:
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
    print(dir(sudoku))
    gameItem = sudoku.buildGridStr(input('Please enter a game string : '))
    runPuzzle(gameItem)
    #runTimedPuzzle(gameItem)