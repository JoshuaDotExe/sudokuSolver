import logging
import os
import json

from src.app.lib.base import base
from src.app.methods.nakedSingles import nakedSingles
from src.app.methods.hiddenSingles import hiddenSingles
from src.app.methods.nakedHidden import nakedHidden
from src.app.methods.pointingSets import pointingSets
from src.app.methods.xWing import xWing

from src.app import textLogo

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
            logging.critical('Board size not supported')
            exit(ValueError)
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