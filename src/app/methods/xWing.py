import logging

from src.app.lib.base import base

class xWing:
    def solveXWing(self: base):
        xWing.__XWingVert(self)
            
        xWing.__XWingHorz(self)
        
    @staticmethod
    def __XWingVert(self: base):
        horzDicts = [self.markNbrDictHorizontal(item) for item in range(self.gridSize)]
        for yCoord, horzDict in enumerate(horzDicts):
            for mark in self.charSet:
                if horzDict[mark] != 2: continue # Only run rows that actually have a chance of holding an xWing
                x = xWing.__markFinder(self.pencilHorizontalNeighbours(yCoord), mark)
                for checkY, checkDict in enumerate(horzDicts):
                    if checkY == yCoord: continue
                    if checkDict[mark] != 2: continue
                    if set(x) != set(xWing.__markFinder(self.pencilHorizontalNeighbours(checkY), mark)): continue
                    y = [yCoord, checkY]
                    if any([xWing.__Elim(self.pencilVerticalNeighbours(x[item]), mark, y) for item in (0, 1)]) == False: continue
                    logging.info(f"SOLVED | X-Wing (vert) | {mark} found in spaces ({x[0]},{y[0]}), ({x[1]},{y[0]}), ({x[0]},{y[1]}), ({x[1]},{y[1]})")
                    return
    
    @staticmethod
    def __XWingHorz(self: base):
        vertDicts = [self.markNbrDictVertical(item) for item in range(self.gridSize)]
        
        for xCoord, vertDict in enumerate(vertDicts):
            for mark in self.charSet:
                if vertDict[mark] != 2: continue
                y = xWing.__markFinder(self.pencilVerticalNeighbours(xCoord), mark)
                for checkX, checkDict in enumerate(vertDicts):
                    if checkX == xCoord: continue
                    if checkDict[mark] != 2: continue
                    if set(y) != set(xWing.__markFinder(self.pencilVerticalNeighbours(checkX), mark)): continue
                    x = [xCoord, checkX]
                    if any([xWing.__Elim(self.pencilHorizontalNeighbours(y[item]), mark, x) for item in (0, 1)]) == False: continue
                    logging.info(f"SOLVED | X-Wing (horz) | {mark} found in spaces ({x[0]},{y[0]}), ({x[1]},{y[0]}), ({x[0]},{y[1]}), ({x[1]},{y[1]})")
                    return
    
    # Used to find the location in a house of the two target items
    @staticmethod
    def __markFinder(targetHouse: list, targetMark: str):
        xCoords = []
        for markIndex, markSpace in enumerate(targetHouse):
            if targetMark not in markSpace: continue
            xCoords.append(markIndex)
        return xCoords
    
    @staticmethod
    def __Elim(targetHouse: list, targetMark: str, whiteList: list):
        notableChange = False
        for targetIndex, targetSpace in enumerate(targetHouse):
            if targetMark not in targetSpace: continue
            if targetIndex in whiteList: continue
            targetSpace.remove(targetMark)
            notableChange = True
        return notableChange