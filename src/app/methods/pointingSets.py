from src.app.lib.base import base
from src import LOGSOLVE

class pointingSets:
    def solvePointingSets(self: base):
        for xCoord in range(self.gridSize):
            pointingSets.__pointingSetsVert(self, xCoord)
            pass
        for yCoord in range(self.gridSize):
            pointingSets.__pointingSetsHorz(self, yCoord)
            pass
        boxCoords = [element*self.subgridSize for element in list(range(self.subgridSize))]
        for xCoord in boxCoords:
            for yCoord in boxCoords:
                pointingSets.__pointingSetsBox(self, xCoord, yCoord)
                pass
    
    @staticmethod
    def __pointingSetsEliminator(target: str, targetBL: list, marksHouse: list):
        notableChange = False
        for markIndex, markSpace in enumerate(marksHouse):
            if markIndex in targetBL:
                continue
            if target in markSpace:
                markSpace.remove(target)
                notableChange = True
        return notableChange
    
    @staticmethod
    def __pointingSetsBox(self: base, x: int, y: int):
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
                if pointingSets.__pointingSetsEliminator(markKey, [item[1] for item in targetList], self.pencilVerticalNeighbours(tempX)):
                    self.turnMoves += 1
                    LOGSOLVE.info(f'POINTING SET (box-vert) | {markKey} found in column {targetList[0][0]} in spaces {tuple(item for item in targetList)}')
                    
            elif all(item[1] == targetList[0][1] for item in targetList) == True:
                if pointingSets.__pointingSetsEliminator(markKey, [item[0] for item in targetList], self.pencilHorizontalNeighbours(tempY)):
                    self.turnMoves += 1
                    LOGSOLVE.info(f'POINTING SET (box-horz) | {markKey} found in row {targetList[0][1]} in spaces {tuple(item for item in targetList)}')
    
    @staticmethod
    def __pointingSetsVert(self: base, x: int):
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
            if pointingSets.__pointingSetsEliminator(markKey, blackList, self.pencilBoxNeighbours(targetList[0], x)) == False:
                continue
            self.turnMoves += 1
            LOGSOLVE.info(f'POINTING SET (vert) | {markKey} found in column {x} in spaces {tuple((x, item) for item in targetList)}')
    
    @staticmethod
    def __pointingSetsHorz(self: base, y: int):
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
            if all(item//self.subgridSize == floorBase for item in targetList) == False:
                continue
            blackList = [item for item in range((y%self.subgridSize)*self.subgridSize, (y%self.subgridSize)*self.subgridSize+self.subgridSize)]
            if pointingSets.__pointingSetsEliminator(markKey, blackList, self.pencilBoxNeighbours(y, targetList[0])) == False:
                continue
            
            self.pencilBoxNeighbours(y, targetList[0])
            self.turnMoves += 1
            LOGSOLVE.info(f'POINTING SET (horz) | {markKey} found in row {y} in spaces {tuple((item, y) for item in targetList)}')