import json
import time

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
        return sudoku.createGame(gameGrid)
    
    @classmethod
    def createGame(cls, gameGrid: list):
        boardSize = len(gameGrid)
        
        ruleOptions = {
            9 : cls.RULE_OF_THREE,
            16 : cls.RULE_OF_FOUR
        }
        
        # Checks if the board is the correct size
        try:
            game = cls(ruleOptions[boardSize])
        except ValueError:
            print(f"Board dimensions {boardSize} not supported")
            raise ValueError
        
        game.grid = gameGrid
        
        # Checks if all values in grid are valid for the grid size chosen
        for row in game.grid:
            if len(row) != int(boardSize):
                print(f"Invalid board: Row {row} too long")
                raise ValueError
            for item in row:
                if item not in game.charSet and item != "0":
                    print(f"Invalid board: Item [{item}] is not a valid character")
                    raise ValueError

        game.removeBasicPencilMarks()
        return game

    # Grid interactions
    # <----------------------------------------------------------------------->

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

    # <----------------------------------------------------------------------->
    # Simple pencil marks interactions
    # <----------------------------------------------------------------------->
    
    def pencilVerticalNeighbours(self, xCoord: int):
        returnList = []
        for row in self.pencilMarks:
            returnList.append(row[xCoord])
        return returnList

    def pencilHorizontalNeighbours(self, yCoord: int):
        returnList = []
        for xValue in self.pencilMarks[yCoord]:
            returnList.append(xValue)
        return returnList
    
    def pencilBoxNeighbours(self, yCoord: int, xCoord: int):
        boxRow = (xCoord//3)*3
        boxCol = (yCoord//3)*3
        returnList = []
        for row in self.pencilMarks[boxCol:boxCol+3]:
            for item in row[boxRow:boxRow+3]:
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

    # <----------------------------------------------------------------------->
    # Logic
    # <----------------------------------------------------------------------->

    def pencilNakedSet(self):
        self.pencilNakedsHorizontal()
        self.pencilNakedsVertical()
        self.pencilNakedsBox()
        
    def pencilNakedsHorizontal(self):
        for yCoord in range(self.gridSize):
            self.nakedActions(self.pencilHorizontalNeighbours(yCoord))

    def pencilNakedsVertical(self):
        for xCoord in range(self.gridSize):
            self.nakedActions(self.pencilVerticalNeighbours(xCoord))

    def pencilNakedsBox(self):
        for xNum in range(self.subgridSize):
            xCoord = xNum * self.subgridSize
            for yNum in range(self.subgridSize):
                yCoord = yNum * self.subgridSize
                self.nakedActions(self.pencilBoxNeighbours(yCoord, xCoord))
    
    def nakedActions(self, house: list):
        # Reminder, a house is a group of values should each be unique
        houseTuples = list()
        for item in house:
            houseTuples.append(tuple(item))
        similarMarks = dict.fromkeys(houseTuples, 0)
        for item in houseTuples:
            similarMarks[item] += 1
        
        # Gets rid of the empty tuple which can really mess with stuff    
        try:   
            similarMarks.pop(())
        except KeyError:
            pass

        for key, value in similarMarks.items():
            # If equal it means the contents of the key can only be in
            # said spaces and should be removed from the rest of the house
            if len(key) == value:
                for item in house:
                    if tuple(item) != key:
                        for symbol in key:
                            try:
                                item.remove(symbol)
                            except ValueError:
                                pass
            
    def reAddPencilMarks(self, workingSet : set):
        for newYCoord in range(len(self.charSet)):
            for newXCoord in range(len(self.charSet)):
                if self.grid[newYCoord][newXCoord] == "0" and len(self.pencilMarks[newYCoord][newXCoord]) == 0:
                    self.pencilMarks[newYCoord][newXCoord] = list(workingSet)

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

    # List of techniques
    def runTechniques(self):
        self.pencilNakedSet()
        self.loneSingles()
        
        self.removeBasicPencilMarks()
        # Add check for only choice in house
        # Add X Y swordfish by checking if the box/row/column has the same number as length of the sets 
        # by turning the check cell into a set and checking for similar subsets, take away the subset from the cell you're checking

    # Checks if only one pencil mark remains 
    # if true it replaces the grid space with it
    def loneSingles(self):
        for yCoord, row in enumerate(self.pencilMarks):
            for xCoord, item in enumerate(row):
                if len(item) == 1:
                    self.grid[yCoord][xCoord] = item[0]
        #self.removeBasicPencilMarks()
    
    # Iterates through grid
    # Finds if any spaces left to solve
    def solvedCheck(self):
        for row in self.grid:
            for item in row:
                if item == "0":
                    return False
        return True        
        
    def solve(self):
        for row in self.grid:
            print(row)
        while self.solved == False:
            #for row in self.grid:
            #    print(row)
            #for row in self.pencilMarks:
            #    print(row)
            #print(f"Turn = {self.turnCounter}")
            #input()
            self.runTechniques()
            self.turnCounter += 1
            
            self.solved = self.solvedCheck()
        for row in self.grid:
            print(row)
        print(f"Solved in {self.turnCounter} turns!")        
            
            
        
def main():
    game = sudoku.loadFromJSON("simple")
    start = time.time_ns()
    game.solve()
    end = time.time_ns()
    print(f"Finished in {(end-start)/1000000}ms")
if __name__ == "__main__":
    main()