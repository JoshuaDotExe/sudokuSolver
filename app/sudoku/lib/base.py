from app.sudoku.lib.pencilMarks import markings

class base(markings):
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
    