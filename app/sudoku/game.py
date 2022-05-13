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
logging.basicConfig(level=logging.CRITICAL,
                    handler=[logging.FileHandler("debug.log"),
                             logging.StreamHandler()])

class sudoku(markings):
    
    def __init__(self, gameGrid):
        
        self.grid = gameGrid
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
    
    def nakedHiddenSets(self):
        for xCoord in range(self.gridSize):
            if self.NHSetsSolver(self.pencilVerticalNeighbours(xCoord), logDesc="vert", x=xCoord): return
        for yCoord in range(self.gridSize):
            if self.NHSetsSolver(self.pencilHorizontalNeighbours(yCoord), logDesc="horz", y=yCoord): return
        boxCoords = [element*self.subgridSize for element in list(range(self.subgridSize))]
        for xCoord in boxCoords:
            for yCoord in boxCoords:
                if self.NHSetsSolver(self.pencilBoxNeighbours(yCoord, xCoord), logDesc="box", x=xCoord, y=yCoord): return
    
    # Removes the found nakedSet from the non subset spaces
    @staticmethod
    def NHSetsEliminator(targetHouse: list, targets: set):
        markElim = False
        for space in targetHouse:
            if frozenset(space).issubset(targets):
                continue
            for target in targets:
                if target in space:
                    space.remove(target)
                    markElim = True
        return markElim
    
    @staticmethod
    def NHSetsDictBuilder(marksHouse: list):
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
                #if len(tempSet) > 4: continue
                verboseSets.append(tempSet)
        frozenSets = [frozenset(item) for item in verboseSets]
        returnDict = dict.fromkeys(frozenSets, 0)
        return returnDict
    
    def NHSetsSolver(self, marksHouse: list, logDesc='NOTSET', x=-1, y=-1):
        marksHouseCopy = deepcopy(marksHouse)
        # Quick non comprehensive test if the house has been fully solved
        # running the solver with an item length of 3 also causes it to
        # see a naked pair when it's actually an unsolvable group of 3
        if all(len(item) <= 2 for item in marksHouseCopy): return False
        # Returns a dict of all possible mark combinations
        possibleSets = self.NHSetsDictBuilder(marksHouseCopy)
        # If there's only one grouping of marks the solver is useless
        for setItem in possibleSets.keys():
            for markItem in marksHouseCopy:
                if markItem == []: continue
                if set(markItem).issubset(setItem):
                    possibleSets[setItem] += 1
        # Looks for naked pairs, triples and quads
        for numSet in (2, 3, 4):
            for setItem, setVal in possibleSets.items():
                if len(setItem) == numSet and setVal == numSet:
                    if self.NHSetsEliminator(marksHouse, setItem) == False:
                        continue
                    self.turnMoves += 1
                    logging.info(f'SOLVED | NAKED SET ({logDesc}) | {tuple(setItem)} found at {f"X = {x}" if x >= 0 else ""}{" , " if x >= 0 and y >= 0 else ""}{f"Y = {y}" if y >= 0 else ""}')
                    return True
        # Looks for hidden pairs, triples and quads
        for numSet in (7, 6, 5):
            for setItem, setVal in possibleSets.items():
                if len(setItem) == numSet and setVal == numSet:
                    if self.NHSetsEliminator(marksHouse, setItem) == False:
                        continue
                    invertedSetItem = set(max(possibleSets.keys(), key=len)).difference(setItem)
                    self.turnMoves += 1
                    logging.info(f'SOLVED | HIDDEN SET ({logDesc}) | {tuple(invertedSetItem)} found at {f"X = {x}" if x >= 0 else ""}{" , " if x >= 0 and y >= 0 else ""}{f"Y = {y}" if y >= 0 else ""}')
                    return True
        return False
    
    def pointingSets(self):
        for xCoord in range(self.gridSize):
            self.pointingSetsVert(xCoord)
        for yCoord in range(self.gridSize):
            self.pointingSetsHorz(yCoord)
        boxCoords = [element*self.subgridSize for element in list(range(self.subgridSize))]
        for xCoord in boxCoords:
            for yCoord in boxCoords:
                self.pointingSetsBox(xCoord, yCoord)
    
    def pointingSetsEliminator(self, target: str, targetBL: list, marksHouse: list):
        notableChange = False
        for markIndex, markSpace in enumerate(marksHouse):
            if markIndex in targetBL:
                continue
            if target in markSpace:
                markSpace.remove(target)
                notableChange = True
        return notableChange
    
    def pointingSetsBox(self, x: int, y: int):
        # If there's only 2 boxes left there's no pointing sets to solve
        # and should be treated as a naked set instead
        marksHouse = self.pencilBoxNeighbours(y, x)
        if all(len(item) < 3 for item in marksHouse): return
        
        markDict = dict.fromkeys(self.charSet, 0)
        for markSpace in marksHouse:
            for item in markSpace:
                markDict[item] += 1
                
        
        for markKey, markVal in markDict.items():
            # Passes the key if there's too many to get a pointing set
            if markVal > self.subgridSize or markVal < 2:
                continue
            targetList = list()
            for markIndex, markSpace in enumerate(marksHouse):
                if markKey not in markSpace:
                    continue
                tempX = x + markIndex%self.subgridSize
                tempY = y + markIndex//self.subgridSize
                targetList.append((tempX, tempY))
            if all(item[0] == targetList[0][0] for item in targetList) == True:
                if self.pointingSetsEliminator(markKey, [item[1] for item in targetList], self.pencilVerticalNeighbours(tempX)):
                    self.turnMoves += 1
                    logging.info(f'SOLVED | POINTING SET (box-vert) | {markKey} found in column {targetList[0][0]} in spaces {tuple(item for item in targetList)}')
                    
            elif all(item[1] == targetList[0][1] for item in targetList) == True:
                if self.pointingSetsEliminator(markKey, [item[0] for item in targetList], self.pencilHorizontalNeighbours(tempY)):
                    self.turnMoves += 1
                    logging.info(f'SOLVED | POINTING SET (box-horz) | {markKey} found in row {targetList[0][1]} in spaces {tuple(item for item in targetList)}')
    
    def pointingSetsVert(self, x: int):
        marksHouse = self.pencilVerticalNeighbours(x)
        if all(len(item) < 3 for item in marksHouse): return
        
        markDict = dict.fromkeys(self.charSet, 0)
        for markSpace in marksHouse:
            for item in markSpace:
                markDict[item] += 1
                
        for markKey, markVal in markDict.items():
            if markVal > self.subgridSize or markVal < 2:
                continue
            targetList = list()
            for markIndex, markSpace in enumerate(marksHouse):
                if markKey not in markSpace:
                    continue
                targetList.append((markIndex))
            floorBase = targetList[0]//self.subgridSize
            if all(item//self.subgridSize == floorBase for item in targetList) == False:
                continue
            
            blackList = [item for item in range(x%self.subgridSize, self.gridSize, self.subgridSize)]
            if self.pointingSetsEliminator(markKey, blackList, self.pencilBoxNeighbours(targetList[0], x)) == False:
                continue
            self.turnMoves += 1
            logging.info(f'SOLVED | POINTING SET (vert) | {markKey} found in column {x} in spaces {tuple(f"({x}, {item})" for item in targetList)}')
    
    def pointingSetsHorz(self, y: int):
        marksHouse = self.pencilHorizontalNeighbours(y)
        if all(len(item) < 3 for item in marksHouse): return
        
        markDict = dict.fromkeys(self.charSet, 0)
        for markSpace in marksHouse:
            for item in markSpace:
                markDict[item] += 1
                
        for markKey, markVal in markDict.items():
            if markVal > self.subgridSize or markVal < 2:
                continue
            targetList = list()
            for markIndex, markSpace in enumerate(marksHouse):
                if markKey not in markSpace:
                    continue
                targetList.append(markIndex)
            floorBase = targetList[0]//self.subgridSize
            if all(item//self.gridSize == floorBase for item in targetList) == False:
                continue
            blackList = [item for item in range(floorBase, floorBase+self.subgridSize)]
            if self.pointingSetsEliminator(markKey, blackList, self.pencilBoxNeighbours(y, targetList[0])) == False:
                continue
            self.turnMoves += 1
            logging.info(f'SOLVED | POINTING SET (horz) | {markKey} found in row {y} in spaces{tuple(f" ({item}, {y})" for item in targetList)}')
    
    def methods(self):
        self.turnCounter += 1
        self.turnMoves = 0
        self.loneSingles()
        self.hiddenSingles()
        
        # If neither of the simple methods work
        if self.turnMoves == 0: self.pointingSets()
        if self.turnMoves == 0: self.nakedHiddenSets()
        
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
        print(self)
        while self.solved == False:
            self.methods()
        
def main():
    
    gameItem = sudoku.buildGridStr(input('Please enter a game string : '))
    gameItem.runPuzzle()

