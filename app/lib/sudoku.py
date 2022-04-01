import json

class sudoku:
    
    RULE_OF_THREE = ('1','2','3','4','5','6','7','8','9')
    RULE_OF_FOUR = ('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f')
    
    def __init__(self, RULE: tuple):
        
        self.gridSize = len(RULE)
        self.grid = list()
        
        self.pencilMarks = [
            [[item for item in RULE] for i in range(self.gridSize)] for x in range(self.gridSize)
            ]
        
        self.charSet = tuple([item for item in RULE])
        self.subgridSize = round(len(self.charSet)**0.5) # Sqrt
        
        self.solved = False
        self.turnCounter = 0
        self.difficulty = 0

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
            for row in self.pencilMarks[fullBox*3:(fullBox*3)+3]:
                for eachThreeItems in range(3):
                    for item in row[eachThreeItems*3:(eachThreeItems*3)+3]:
                        printStr += f'{item} '
                    printStr += '   '
                printStr += '\n'
            if fullBox < 2:
                printStr += '\n'
        
        printStr += f"Turns taken = {self.turnCounter}"
        return printStr
    
    # Constructor
    @classmethod
    def loadFromJSON(cls, fileName: str):
        
        with open(f"app/resources/premadeGames/{fileName}.json", "r") as file:
            gameGrid = json.load(file)["grid"]
        boardSize = len(gameGrid)
        
        ruleOptions = {
            9 : cls.RULE_OF_THREE,
            16 : cls.RULE_OF_FOUR
        }
        
        # Checks if the board is the correct size
        try:
            classItem = cls(ruleOptions[boardSize])
        except ValueError:
            print(f"Board dimensions {boardSize} not supported")
            raise ValueError
        
        classItem.grid = gameGrid
        
        # Checks if all values in grid are valid for the grid size chosen
        for row in classItem.grid:
            if len(row) != int(boardSize):
                print(f"Invalid board: Row {row} too long")
                raise ValueError
            for item in row:
                if item not in classItem.charSet and item != "0":
                    print(f"Invalid board: Item [{item}] is not a valid character")
                    raise ValueError

        classItem.initPencilMarks()
        classItem.removeBasicPencilMarks()
        return classItem
    
    def initPencilMarks(self):
        for rowIndex in range(self.gridSize):
            for colIndex in range(self.gridSize):
                if self.grid[rowIndex][colIndex] != '0':
                    self.pencilMarks[rowIndex][colIndex] = []
                    
    def verticalNeighbours(self, xCoord: int):
        returnList = []
        for row in self.grid:
            if row[xCoord] != "0":
                returnList.append(row[xCoord])
        return returnList
    
    def horizontalNeighbours(self, yCoord: int):
        returnList = []
        for xValue in self.grid[yCoord]:
            if xValue != "0":
                returnList.append(xValue)
        return returnList
    
    def boxNeighbours(self, yCoord: int, xCoord: int):
        boxRow = (xCoord//3)*3
        boxCol = (yCoord//3)*3
        returnList = []
        for row in self.grid[boxCol:boxCol+3]:
            for item in row[boxRow:boxRow+3]:
                if item != "0":
                    returnList.append(item)
        return returnList
    
    def pencilVerticalNeighbours(self, xCoord: int):
        returnList = []
        for row in self.pencilMarks:
            if len(row[xCoord]) != 0:
                returnList.append(row[xCoord])
        return returnList

    def pencilHorizontalNeighbours(self, yCoord: int):
        returnList = []
        for xValue in self.pencilMarks[yCoord]:
            if len(xValue) != 0:
                returnList.append(xValue)
        return returnList
    
    def pencilBoxNeighbours(self, yCoord: int, xCoord: int):
        boxRow = (xCoord//3)*3
        boxCol = (yCoord//3)*3
        returnList = []
        for row in self.pencilMarks[boxCol:boxCol+3]:
            for item in row[boxRow:boxRow+3]:
                if len(item) != 0:
                    returnList.append(item)
        return returnList
    
    def pencilNeighboursDict(self, yCoord: int, xCoord: int) -> dict: 
        neighbourDict = dict.fromkeys(self.charSet, 0)
            
        # Adds item in row
        for itemList in self.pencilHorizontalNeighbours(yCoord):
            for item in itemList:
                neighbourDict[item] += 1
            
        # Adds items in col
        for itemList in self.pencilVerticalNeighbours(xCoord):
            for item in itemList:
                neighbourDict[item] += 1
            
        # Adds items in box
        for itemList in self.pencilBoxNeighbours(yCoord, xCoord):
            for item in itemList:
                neighbourDict[item] += 1
        
        return neighbourDict
    
    def pencilNeighboursList(self, yCoord: int, xCoord: int):
        returnList = []
        
        # Adds item in row
        for itemList in self.pencilHorizontalNeighbours(yCoord):
            returnList.append(itemList)
            
        # Adds items in col
        for itemList in self.pencilVerticalNeighbours(xCoord):
            returnList.append(itemList)
            
        # Adds items in box
        for itemList in self.pencilBoxNeighbours(yCoord, xCoord):
            returnList.append(itemList)
        
        return returnList
        
    def solveCrossHatchScanning(self, yCoord: int, xCoord: int) -> str:
        for checkItem in self.pencilMarks[yCoord][xCoord]:
            compareDict = self.pencilNeighboursDict(yCoord, xCoord)
            if compareDict[checkItem] == 3:
                print(f"{checkItem} valid in {yCoord}, {xCoord}")
                return checkItem
        return "0"
    
    def pencilNakedPair(self, yCoord: int, xCoord: int):
        curSpaceSet = set(self.pencilMarks[yCoord][xCoord])
        spaceSetLength = len(curSpaceSet)
        
        boxRow = (xCoord//3)*3
        boxCol = (yCoord//3)*3
        
        counter = 0
        for itemList in self.pencilBoxNeighbours(yCoord, xCoord):
            if curSpaceSet == set(itemList):
                counter += 1
        
        if counter != spaceSetLength:
            return
        for item in curSpaceSet:
            self.removePencilMarksBox(item, xCoord, yCoord)
        
        self.reAddPencilMarks(curSpaceSet)
        coordList = []
        
        
        subYCount = 0
        for row in self.pencilMarks[boxCol:boxCol+3]:
            subXCount = 0
            for item in row[boxRow:boxRow+3]:
                if set(item) == curSpaceSet:
                    coordList.append([subYCount, subXCount])
                subXCount += 1
            subYCount += 1
        # Horizontal and vertical checkers arent working, pls fix :(
        
        # Checks if all horizontally alligned
        if all(x[0] == coordList[0][0] for x in coordList) == True:
            for item in curSpaceSet:
                print(f"Attempting to remove {item} in row {yCoord}")
                self.removePencilMarksHorizontal(item, yCoord)
                self.reAddPencilMarks(curSpaceSet)
            
        
        # Checks if all vertically alligned
        if all(x[1] == coordList[0][1] for x in coordList) == True:
            for item in curSpaceSet:
                print(f"Attempting to remove {item} in column {xCoord}")
                self.removePencilMarksVertical(item, xCoord)
                self.reAddPencilMarks(curSpaceSet)

    def removePencilMarksVertical(self, target: str, xCoord: int):
        for row in self.pencilMarks:
            try:
                row[xCoord].remove(target)
            except ValueError:
                pass
    
    def removePencilMarksHorizontal(self, target: str, yCoord: int):
        for item in self.pencilMarks[yCoord]:
            try:
                item.remove(target)
            except ValueError:
                pass
    
    def removePencilMarksBox(self, target: str, xCoord: int, yCoord: int):
        boxRow = (yCoord//3)*3
        boxCol = (xCoord//3)*3
        for row in self.pencilMarks[boxRow:boxRow+3]:
            for item in row[boxCol:boxCol+3]:
                try:
                    item.remove(target)
                except ValueError:
                    pass

    # Uses solved spaces to reduce the pencil marks
    # Technically solves for hidden singles
    def removeBasicPencilMarks(self):
        for yCoord, row in enumerate(self.grid):
            for xCoord, item in enumerate(row):
                if item != '0':
                    self.removePencilMarksBox(item, xCoord, yCoord)
                    self.removePencilMarksHorizontal(item, yCoord)
                    self.removePencilMarksVertical(item, xCoord)
                    self.pencilMarks[yCoord][xCoord] = []

    def reAddPencilMarks(self, workingSet : set):
        for newYCoord in range(len(self.charSet)):
            for newXCoord in range(len(self.charSet)):
                if self.grid[newYCoord][newXCoord] == "0" and len(self.pencilMarks[newYCoord][newXCoord]) == 0:
                    self.pencilMarks[newYCoord][newXCoord] = list(workingSet)

    def runTechniques(self):
        self.nakedSingles()
        
        #for yCoord, row in enumerate(self.pencilMarks):
        #    for xCoord, item in enumerate(row):
                # Checks to see if it has a unique pencil mark in its box, row and column
                #if len(self.pencilMarks[yCoord][xCoord]) > 1:
                #    self.grid[yCoord][xCoord] = self.solveCrossHatchScanning(yCoord, xCoord)
                # Runs naked pair technique
                #if len(self.pencilMarks[yCoord][xCoord]) == 2:
                #    self.pencilNakedPair(yCoord, xCoord)

    # Checks if only one pencil mark remains 
    # if true it replaces the grid space with it
    def nakedSingles(self):
        for yCoord, row in enumerate(self.pencilMarks):
            for xCoord, item in enumerate(row):
                if len(item) == 1:
                    self.grid[yCoord][xCoord] = item[0]
                    self.removeBasicPencilMarks()
    
    # Iterates through grid
    # Finds if any spaces left to solve
    def solvedCheck(self):
        for row in self.grid:
            for item in row:
                if item == "0":
                    return False
        return True        
        
    def solve(self):
        while self.solved == False:
            for row in self.grid:
                print(row)
            for row in self.pencilMarks:
                print(row)
            print(f"Turn = {self.turnCounter}")
            input()
            self.runTechniques()
            
            self.turnCounter += 1
            
            self.solved = self.solvedCheck()
        for row in self.grid:
            print(row)
        print(f"Solved in {self.turnCounter} turns!")        
            
            
        
def main():
    game = sudoku.loadFromJSON("easy")
    game.solve()

if __name__ == "__main__":
    main()