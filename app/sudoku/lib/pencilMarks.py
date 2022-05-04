class markings:
    rules = {
            4 : ('1','2','3','4'),
            9 : ('1','2','3','4','5','6','7','8','9'),
            16 : ('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f')
        }
    def __init__(self, gameSize :int):
        self.charSet = self.buildCharSet(gameSize)
        self.marks = self.buildMarkingGrid(gameSize)
        
    @classmethod
    def buildCharSet(cls, dimension: int):
        return markings.rules[dimension]
    
    @classmethod
    def buildMarkingGrid(cls, dimension: int):
        marks = list()
        for _ in range(dimension):
            row = list()
            for _ in range(dimension):
                row.append(list(cls.rules[dimension]))
            marks.append(row)
        return marks
    
    def pencilVerticalNeighbours(self, xCoord: int):
        returnList = []
        for row in self.marks:
            returnList.append(row[xCoord])
        return returnList

    def pencilHorizontalNeighbours(self, yCoord: int):
        returnList = []
        for xValue in self.marks[yCoord]:
            returnList.append(xValue)
        return returnList
    
    def pencilBoxNeighbours(self, yCoord: int, xCoord: int):
        boxRow = (xCoord//3)*3
        boxCol = (yCoord//3)*3
        returnList = []
        for row in self.marks[boxCol:boxCol+3]:
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
    
    def pencilNeighboursSet(self, yCoord: int, xCoord: int) -> dict: 
        neighbourSet = set()
            
        # Adds item in row
        for itemList in self.pencilHorizontalNeighbours(yCoord):
            for item in itemList:
                neighbourSet.update(item)
            
        # Adds items in col
        for itemList in self.pencilVerticalNeighbours(xCoord):
            for item in itemList:
                neighbourSet.update(item)
            
        # Adds items in box
        for itemList in self.pencilBoxNeighbours(yCoord, xCoord):
            for item in itemList:
                neighbourSet.update(item)
        
        return neighbourSet
        
    def removeMarksVertical(self, target: str, xCoord: int):
        for row in self.marks:
            try:
                row[xCoord].remove(target)
            except ValueError:
                pass
    
    def removeMarksHorizontal(self, target: str, yCoord: int):
        for item in self.marks[yCoord]:
            try:
                item.remove(target)
            except ValueError:
                pass
    
    def removeMarksBox(self, target: str, xCoord: int, yCoord: int):
        boxRow = (yCoord//3)*3
        boxCol = (xCoord//3)*3
        for row in self.marks[boxRow:boxRow+3]:
            for item in row[boxCol:boxCol+3]:
                try:
                    item.remove(target)
                except ValueError:
                    pass
