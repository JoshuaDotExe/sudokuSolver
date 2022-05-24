import logging
import os
import json

from src.app.lib.base import base
from src.app.methods.nakedSingles import nakedSingles
from src.app.methods.hiddenSingles import hiddenSingles
from src.app.methods.nakedHidden import nakedHidden
from src.app.methods.pointingSets import pointingSets
from src.app.methods.xWing import xWing

from src import LOGDEBUG, LOGSOLVE

class sudoku(base, nakedSingles, hiddenSingles, nakedHidden, pointingSets, xWing):
    def methods(self):
        self.turnCounter += 1
        self.turnMoves = 0
        self.solveNakedSingles()
        self.solveHiddenSingles()
        
        # If neither of the simple methods work
        if self.turnMoves == 0: self.solvePointingSets()
        if self.turnMoves == 0: self.solveNakedHiddenSets()
        if self.turnMoves == 0: self.solveXWing()
        self.removeBasicMarks()
        
    # Iterates through grid
    # Finds if any spaces left to solve
    def solvedCheck(self):
        for row in self.grid:
            for item in row:
                if item == "0":
                    return False
        return True
        
    @staticmethod
    def buildGridJSON(filename = 'easy'):
        cwd = os.getcwd().replace("\\", "/") 
        targetDir = cwd + f"/app/resources/premadeGames/{filename}.json"
        with open(targetDir, "r") as file:
            gameGrid = json.load(file)["grid"]
        return sudoku(gameGrid)
    
    @staticmethod
    def buildGridStr(inputStr: str):
        strLength = len(inputStr)
        strSqrt = round(strLength**0.5)
        if strLength not in (16, 81, 256):
            LOGDEBUG.critical('Board size not supported')
        counter = 0
        gameGrid = []
        for _ in range(strSqrt):
            tempList = []
            for item in inputStr[counter:counter+strSqrt]:
                if item in ('0', '.', ' ', '*'):
                    tempList.append('0')
                    continue
                tempList.append(item)
            counter += strSqrt
            gameGrid.append(tempList)
        return sudoku(gameGrid)
    
    def solveOnce(self):
        LOGSOLVE.info('Running single method...')
        self.methods()
        if self.turnMoves == 0:
            self.solved = True
            LOGSOLVE.warning("Game Currently Unsolvable")
            LOGDEBUG.warning('Required method not available')
            return True
        elif self.solvedCheck() == True:
            self.solved = True
            LOGSOLVE.info("Game Solved")
            return True
        return False
    
    def solveFull(self):
        LOGSOLVE.info('Running methods to completion...')
        while self.solved == False:
            self.methods()
            if self.turnMoves == 0:
                self.solved = True
                LOGSOLVE.warning("Game Currently Unsolvable")
                LOGDEBUG.warning('Required method not available')
            if self.solvedCheck() == True:
                self.solved = True
                LOGSOLVE.info("Game Solved")
        
        
        