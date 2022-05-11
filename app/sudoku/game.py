import json
import logging
import os
from copy import deepcopy

from app.sudoku.lib.pencilMarks import markings
from app import __version__
from app.sudoku import textLogo

logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.FileHandler("debug.log"),
                              logging.StreamHandler()])
logging.basicConfig(level=logging.INFO,
                    handler=[logging.FileHandler("debug.log"),
                             logging.StreamHandler()])
logging.basicConfig(level=logging.WARNING,
                    handler=[logging.FileHandler("debug.log"),
                             logging.StreamHandler()])

class sudoku(markings):
    
    def __init__(self, fileName="easy"):
        
        self.grid = self.buildGridJSON(fileName)
        self.gridSize = len(self.grid)
        self.subgridSize = round(self.gridSize**0.5) # Sqrt
        
        self.solved = False
        self.turnCounter = 0
        self.difficulty = 0
        
        self.turnMoves = 0
        
        super().__init__(self.gridSize)
        self.removeBasicMarks()
    
    def __str__(self):
        printStr = str()
        # Defines major grid lines
        illegalGridlines = list(range(self.subgridSize))
        for num in range(self.subgridSize):
            illegalGridlines[num] = ((illegalGridlines[num]+1)*self.subgridSize)-1
        
        for rowNum, row in enumerate(self.grid):
            for subline in range(self.subgridSize):
                for colNum, item in enumerate(row):
                    if item != "0":
                        if subline == 1:
                            printStr += f"  {item}  "
                        else:
                            printStr += "     "
                    else:
                        # Prints out the marks if no number present in space
                        printStr += " "
                        for num in range(self.subgridSize):
                            targetChar = self.charSet[num + self.subgridSize*subline]
                            printStr += targetChar if targetChar in self.marks[rowNum][colNum] else " "
                        printStr += " "
                    if colNum not in illegalGridlines:
                        printStr += " | "  
                    else:
                        if colNum != self.gridSize-1:
                            printStr += " / "
                printStr += "\n"
            if rowNum in illegalGridlines:
                if rowNum == self.gridSize-1:
                    printStr += "\n"
                    continue
                for gridTrack in range(self.gridSize):
                    for _ in range(self.subgridSize+2):
                        printStr += "/"
                    if gridTrack != self.gridSize-1:
                        for _ in range(self.subgridSize):
                            printStr += "/"
                printStr += "\n"
                continue
            
            # Makes horizontal minor grid lines
            for gridTrack in range(self.gridSize):
                for _ in range(self.subgridSize+2):
                    printStr += "-"
                if gridTrack not in illegalGridlines:
                    for _ in range(self.subgridSize):
                        printStr += "-"
                else:
                    if gridTrack != self.gridSize-1:
                        printStr += " / "
            printStr += "\n"
        printStr += f"Turns taken = {self.turnCounter}\n"
        return printStr
    
    @staticmethod
    def buildGridJSON(filename: str):
        cwd = os.getcwd().replace("\\", "/") 
        targetDir = cwd + f"/app/resources/premadeGames/{filename}.json"
        with open(targetDir, "r") as file:
            gameGrid = json.load(file)["grid"]
        return gameGrid
    
    def verticalNeighbours(self, xCoord: int):
        returnList = []
        for row in self.grid:
            returnList.append(row[xCoord])
        return returnList
    
    def horizontalNeighbours(self, yCoord: int):
        returnList = []
        for xValue in self.grid[yCoord]:
            returnList.append(xValue)
        return returnList
    
    def boxNeighbours(self, yCoord: int, xCoord: int):
        boxRow = (xCoord//3)*3
        boxCol = (yCoord//3)*3
        returnList = []
        for row in self.grid[boxCol:boxCol+3]:
            for item in row[boxRow:boxRow+3]:
                returnList.append(item)
        return returnList
    
    # Uses solved spaces to reduce the pencil marks
    # Technically solves for hidden singles
    def removeBasicMarks(self):
        for yCoord, row in enumerate(self.grid):
            for xCoord, item in enumerate(row):
                if item != '0':
                    self.removeMarkBox(item, xCoord, yCoord)
                    self.removeMarkHorizontal(item, yCoord)
                    self.removeMarkVertical(item, xCoord)
                    self.marks[yCoord][xCoord] = []
    
    
    # Checks if only one pencil mark remains in each space
    # if true it replaces the grid space with it
    def loneSingles(self):
        totalMoves = 0
        for yCoord, row in enumerate(self.marks):
            for xCoord, item in enumerate(row):
                if len(item) == 1:
                    self.grid[yCoord][xCoord] = item[0]
                    self.turnMoves += 1
                    logging.info(f"SOLVED | LONE SINGLE | Space ({xCoord},{yCoord}) is a {item[0]}")
        self.removeBasicMarks()
        return totalMoves
    
    
    # Checks if only one type of mark remains in each house
    # if true it replaces the grid space with it
    def hiddenSingles(self):
        for xCoord in range(self.gridSize):
            self.hiddenSinglesVertical(xCoord)
        for yCoord in range(self.gridSize):
            self.hiddenSinglesHorizontal(yCoord)
        boxCoords = [element*self.subgridSize for element in list(range(self.subgridSize))]
        for xCoord in boxCoords:
            for yCoord in boxCoords:
                self.hiddenSinglesBox(xCoord, yCoord)
        
    def hiddenSinglesVertical(self, xCoord : int):
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
                    logging.info(f"SOLVED | HIDDEN SINGLE (vert)| Space ({xCoord},{yCoord}) is a {target}")
                    self.turnMoves += 1
        self.removeBasicMarks()
    
    def hiddenSinglesHorizontal(self, yCoord : int):
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
                    logging.info(f"SOLVED | HIDDEN SINGLE (horz)| Space ({xCoord},{yCoord}) is a {target}")
                    self.turnMoves += 1
        self.removeBasicMarks()
    
    def hiddenSinglesBox(self, xCoord : int, yCoord : int):
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
                    logging.info(f"SOLVED | HIDDEN SINGLE (box)| Space ({tempX},{tempY}) is a {target}")
                    self.turnMoves += 1
        self.removeBasicMarks()
    
    def nakedSets(self):
        for xCoord in range(self.gridSize):
            if self.nakedSetsSolver(self.pencilVerticalNeighbours(xCoord), logDesc="vert", x=xCoord): return
        for yCoord in range(self.gridSize):
            if self.nakedSetsSolver(self.pencilHorizontalNeighbours(yCoord), logDesc="horz", y=yCoord): return
        boxCoords = [element*self.subgridSize for element in list(range(self.subgridSize))]
        for xCoord in boxCoords:
            for yCoord in boxCoords:
                if self.nakedSetsSolver(self.pencilBoxNeighbours(yCoord, xCoord), logDesc="box", x=xCoord, y=yCoord): return
    
    # Removes the found nakedSet from the non subset spaces
    @staticmethod
    def nakedSetsEliminator(targetHouse: list, targets: set):
        markElim = False
        for space in targetHouse:
            if frozenset(space).issubset(targets):
                continue
            for target in targets:
                if target in space:
                    space.remove(target)
                    markElim = True
        return markElim
    
    # @staticmethod
    # def nakedSetsCheckSets(marksHouseCopy: list):
    #     # Removes all empty spaces to make it easier to search for valid naked sets
    #     sortedHouse = list(filter(lambda houseItem: len(houseItem) != 0, marksHouseCopy))
    #     # Creates a set of items which grows at x*len(sortedHouse)
    #     # to contain a list of all possible combinations
    #     baseSets = [set(item) for item in sortedHouse]
    #     checkSets = []
    #     for markNum, markSet in enumerate(baseSets):
    #         for adjustIndex in range(len(sortedHouse)):
    #             if markNum == adjustIndex: continue
    #             markSetCopy = deepcopy(markSet)
    #             markSetCopy.update(set(sortedHouse[(markNum+adjustIndex)%len(sortedHouse)]))
    #             checkSets.append(markSetCopy)
    #     frozenSets = [frozenset(item) for item in checkSets]
    #     checkSets = [set(item) for item in list(set(frozenSets))]
    #     return checkSets
    
    @staticmethod
    def nakedSetsDictBuilder(marksHouse: list):
        # Removes all empty spaces to make it easier to search for valid naked sets
        cleanedHouse = list(filter(lambda houseItem: len(houseItem) != 0, marksHouse))
        cleanedSets = [set(item) for item in cleanedHouse]
        # Creates a set of items which grows at x*len(sortedHouse)
        # to contain a list of all possible combinations
        # Combines every space with every space apart from its own as a set
        # Used to create a list of all viable sets
        verboseSets = []
        for markSet in cleanedSets:
            cleanedCopy = deepcopy(cleanedSets)
            cleanedCopy.remove(markSet)
            for tempIndex in range(len(cleanedHouse)-1):
                tempSet = deepcopy(markSet)
                tempSet.update(set(cleanedHouse[tempIndex]))
                if len(tempSet) > 4: continue
                verboseSets.append(tempSet)
        frozenSets = [frozenset(item) for item in verboseSets]
        returnDict = dict.fromkeys(frozenSets, 0)
        return returnDict
    
    def nakedSetsSolver(self, marksHouse: list, logDesc='NOTSET', x=-1, y=-1):
        marksHouseCopy = deepcopy(marksHouse)
        # Quick non comprehensive test if the house has been fully solved
        # running the solver with an item length of 3 also causes it to
        # see a naked pair when it's actually an unsolvable group of 3
        if all(len(item) <= 2 for item in marksHouseCopy): return False
        # Returns a dict of all possible mark combinations
        possibleSets = self.nakedSetsDictBuilder(marksHouseCopy)
        # If there's only one grouping of marks the solver is useless
        for setItem in possibleSets.keys():
            for markItem in marksHouseCopy:
                if markItem == []: continue
                if set(markItem).issubset(setItem):
                    possibleSets[setItem] += 1
        # Only looks for pairs, triples and quads, no quints
        for numSet in (2, 3, 4):
            for setItem, setVal in possibleSets.items():
                if len(setItem) == numSet and setVal == numSet:
                    if self.nakedSetsEliminator(marksHouse, setItem) == False:
                        continue
                    self.turnMoves += 1
                    logging.info(f'SOLVED | NAKED SET ({logDesc})| {tuple(setItem)} found at {f"X = {x}" if x >= 0 else ""}{" , " if x >= 0 and y >= 0 else ""}{f"Y = {y}" if y >= 0 else ""}')
                    return True
        return False
    
    # def nakedSetsVert(self, xCoord: int):
    #     marksHouse = self.pencilVerticalNeighbours(xCoord)
    #     marksHouseCopy = deepcopy(marksHouse)
    #     # Quick non comprehensive test if the house has been fully solved
    #     # running the solver with an item length of 3 also causes it to
    #     # see a naked pair when it's actually an unsolvable group of 3
    #     if all(len(item) <= 3 for item in marksHouseCopy): return False
    #     # Returns if the set that remains solves nothing, ie it's the last thing that remains
    #     checkSets = self.nakedSetsCheckSets(marksHouseCopy)
    #     if len(checkSets) == 1: return False
    #     # Only looks for pairs, triples and quads, no quints
    #     for numSet in (2, 3, 4):
    #         for checkSet in checkSets:
    #             if len(checkSet) == numSet:
    #                 if self.nakedSetsEliminator(marksHouse, checkSet) == True:
    #                     self.turnMoves += 1
    #                     logging.info(f'SOLVED | NAKED SET (vert)| {checkSet} found at X = {xCoord}')
    #                     return True
    #     return False
                        
    # def nakedSetsHorz(self, yCoord: int):
    #     marksHouse = self.pencilHorizontalNeighbours(yCoord)
    #     marksHouseCopy = deepcopy(marksHouse)
    #     if all(len(item) <= 3 for item in marksHouseCopy):
    #         return
    #     checkSets = self.nakedSetsCheckSets(marksHouseCopy)
    #     if len(checkSets) == 1:
    #         return
    #     for numSet in (2, 3, 4):
    #         for checkSet in checkSets:
    #             if len(checkSet) == numSet:
    #                 if self.nakedSetsEliminator(marksHouse, checkSet) == True:
    #                     self.turnMoves += 1
    #                     logging.info(f'SOLVED | NAKED SET (horz)| {checkSet} found at Y = {yCoord}')
    #                     return True
    #     return False
    
    # def nakedSetsBox(self, xCoord: int, yCoord: int):
    #     marksHouse = self.pencilBoxNeighbours(yCoord, xCoord)
    #     marksHouseCopy = deepcopy(marksHouse)
    #     if all(len(item) <= 3 for item in marksHouseCopy):
    #         return False
    #     checkSets = self.nakedSetsCheckSets(marksHouseCopy)
    #     if len(checkSets) == 1:
    #         return False
    #     for numSet in (2, 3, 4):
    #         for checkSet in checkSets:
    #             if len(checkSet) == numSet:
    #                 if self.nakedSetsEliminator(marksHouse, checkSet) == True:
    #                     self.turnMoves += 1
    #                     logging.info(f'SOLVED | NAKED SET (box)| {checkSet} found at X = {xCoord}, Y = {yCoord}')
    #                     return True
    #     return False
    
    
    def methods(self):
        self.turnCounter += 1
        self.turnMoves = 0
        self.loneSingles()
        self.hiddenSingles()
        
        # If neither of the simple methods work
        if self.turnMoves == 0:
            self.nakedSets()
        
        if self.turnMoves == 0:
            self.solved = True
            logging.warning("Game Currently Unsolvable")
            return
        if self.solvedCheck() == True:
            self.solved = True
            logging.info("Game Solved")
            print(self)
            return
    
    # Iterates through grid
    # Finds if any spaces left to solve
    def solvedCheck(self):
        for row in self.grid:
            for item in row:
                if item == "0":
                    return False
        return True
    
    def runPuzzle(self):
        print(f"Running Sudoku Solver : Version # {__version__}")
        print(textLogo)
        while self.solved == False:
            print(self)
            input()
            self.methods()
        
def main():
    gameItem = sudoku()
    gameItem.runPuzzle()

