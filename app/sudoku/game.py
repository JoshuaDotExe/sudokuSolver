import json
import logging
import os

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
    
    def __init__(self, fileName="medium"):
        
        self.grid = self.buildGridJSON(fileName)
        self.gridSize = len(self.grid)
        self.subgridSize = round(self.gridSize**0.5) # Sqrt
        
        self.solved = False
        self.turnCounter = 0
        self.difficulty = 0
        
        self.turnMoves = 0
        
        super().__init__(self.gridSize)
        self.removeBasicMarks()

    def __repr__(self):
        printStr = ""
        for fullBox in range(3):
            for row in self.grid[fullBox*3:(fullBox*3)+3]:
                for eachThreeItems in range(3):
                    for item in row[eachThreeItems*3:(eachThreeItems*3)+3]:
                        printStr += f'{item} '
                    printStr += '   '
                printStr += '\n'
            if fullBox < 2:
                printStr += '\n'
        
        printStr += '\n'
        
        for fullBox in range(3):
            for row in self.marks[fullBox*3:(fullBox*3)+3]:
                for eachThreeItems in range(3):
                    for item in row[eachThreeItems*3:(eachThreeItems*3)+3]:
                        printStr += f'{item} '
                    printStr += '   '
                printStr += '\n'
            if fullBox < 2:
                printStr += '\n'
        
        printStr += f"Turns taken = {self.turnCounter}"
        return printStr
    
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
        print(boxCoords)
        for xCoord in boxCoords:
            for yCoord in boxCoords:
                self.hiddenSinglesBox(xCoord, yCoord)
                #pass
        
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
                    
    def methods(self):
        self.turnMoves = 0
        self.loneSingles()
        self.hiddenSingles()
        
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

