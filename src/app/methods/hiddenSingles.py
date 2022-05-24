from src.app.lib.base import base
from src import LOGSOLVE

class hiddenSingles:
    # Checks if only one type of mark remains in each house
    # if true it replaces the grid space with it
    def solveHiddenSingles(self: base):
        for xCoord in range(self.gridSize):
            hiddenSingles.__hiddenSinglesVertical(self, xCoord)
        for yCoord in range(self.gridSize):
            hiddenSingles.__hiddenSinglesHorizontal(self, yCoord)
        boxCoords = [element*self.subgridSize for element in list(range(self.subgridSize))]
        for xCoord in boxCoords:
            for yCoord in boxCoords:
                hiddenSingles.__hiddenSinglesBox(self, xCoord, yCoord)
    
    @staticmethod
    def __hiddenSinglesVertical(self: base, xCoord : int):
        targets = list()
        for targetNum, numerator in self.markNbrDictVertical(xCoord).items():
            if numerator == 1:
                targets.append(targetNum)
        if len(targets) == 0:
            return
        for target in targets:
            for yCoord, markList in enumerate(self.pencilVerticalNeighbours(xCoord)):
                if target in markList:
                    self.grid[yCoord][xCoord] = target
                    LOGSOLVE.info(f"HIDDEN SINGLE (vert)| Space ({xCoord},{yCoord}) is a {target}")
                    self.turnMoves += 1
        self.removeBasicMarks()
    
    @staticmethod
    def __hiddenSinglesHorizontal(self: base, yCoord : int):
        targets = list()
        for targetNum, numerator in self.markNbrDictHorizontal(yCoord).items():
            if numerator == 1:
                targets.append(targetNum)
        if len(targets) == 0:
            return
        for target in targets:
            for xCoord, markList in enumerate(self.pencilHorizontalNeighbours(yCoord)):
                if target in markList:
                    self.grid[yCoord][xCoord] = target
                    LOGSOLVE.info(f"HIDDEN SINGLE (horz) | Space ({xCoord},{yCoord}) is a {target}")
                    self.turnMoves += 1
        self.removeBasicMarks()
    
    @staticmethod
    def __hiddenSinglesBox(self: base, xCoord : int, yCoord : int):
        targets = list()
        for targetNum, numerator in self.markNbrDictBox(xCoord, yCoord).items():
            if numerator == 1:
                targets.append(targetNum)
        if len(targets) == 0:
            return
        for target in targets:
            for count, markList in enumerate(self.pencilBoxNeighbours(yCoord, xCoord)):
                if target in markList:
                    tempX = ((xCoord//self.subgridSize)*self.subgridSize)+count%self.subgridSize
                    tempY = ((yCoord//self.subgridSize)*self.subgridSize)+count//self.subgridSize
                    self.grid[tempY][tempX] = target
                    LOGSOLVE.info(f"HIDDEN SINGLE (box) | Space ({tempX},{tempY}) is a {target}")
                    self.turnMoves += 1
        self.removeBasicMarks()