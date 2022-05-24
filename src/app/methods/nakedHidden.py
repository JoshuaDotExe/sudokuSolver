from copy import deepcopy

from src.app.lib.base import base
from src import LOGSOLVE, LOGDEBUG

class nakedHidden:
    def solveNakedHiddenSets(self: base):
        for xCoord in range(self.gridSize):
            if nakedHidden.__NHSetsSolver(self, self.pencilVerticalNeighbours(xCoord), logDesc="vert", x=xCoord): return
        for yCoord in range(self.gridSize):
            if nakedHidden.__NHSetsSolver(self, self.pencilHorizontalNeighbours(yCoord), logDesc="horz", y=yCoord): return
        boxCoords = [element*self.subgridSize for element in list(range(self.subgridSize))]
        for xCoord in boxCoords:
            for yCoord in boxCoords:
                if nakedHidden.__NHSetsSolver(self, self.pencilBoxNeighbours(yCoord, xCoord), logDesc="box", x=xCoord, y=yCoord): return
    
    # Removes the found nakedSet from the non subset spaces
    @staticmethod
    def __NHSetsEliminator(targetHouse: list, targets: set):
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
    def __NHSetsDictBuilder(marksHouse: list):
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
    
    @staticmethod
    def __NHSetsSolver(self: base, marksHouse: list, logDesc='NOTSET', x=-1, y=-1):
        marksHouseCopy = deepcopy(marksHouse)
        # Quick non comprehensive test if the house has been fully solved
        # running the solver with an item length of 3 also causes it to
        # see a naked pair when it's actually an unsolvable group of 3
        if all(len(item) <= 2 for item in marksHouseCopy): return False
        # Returns a dict of all possible mark combinations
        possibleSets = nakedHidden.__NHSetsDictBuilder(marksHouseCopy)
        # If there's only one grouping of marks the solver is useless
        logSetID = {2:'Pair', 3:'Triple', 4:'Quad'}
        for setItem in possibleSets.keys():
            for markItem in marksHouseCopy:
                if markItem == []: continue
                if set(markItem).issubset(setItem):
                    possibleSets[setItem] += 1
        # Looks for naked pairs, triples and quads
        for numSet in (2, 3, 4):
            for setItem, setVal in possibleSets.items():
                if len(setItem) == numSet and setVal == numSet:
                    if nakedHidden.__NHSetsEliminator(marksHouse, setItem) == False:
                        continue
                    self.turnMoves += 1
                    LOGSOLVE.info(f'NAKED {logSetID[len(setItem)]} ({logDesc}) | {tuple(setItem)} found at {f"X = {x}" if x >= 0 else ""}{" , " if x >= 0 and y >= 0 else ""}{f"Y = {y}" if y >= 0 else ""}')
                    return True
        # Looks for hidden pairs, triples and quads
        for numSet in (7, 6, 5):
            for setItem, setVal in possibleSets.items():
                if len(setItem) == numSet and setVal == numSet:
                    if nakedHidden.__NHSetsEliminator(marksHouse, setItem) == False:
                        continue
                    invertedSetItem = set(max(possibleSets.keys(), key=len)).difference(setItem)
                    self.turnMoves += 1
                    LOGSOLVE.info(f'HIDDEN {logSetID[len(invertedSetItem)]} ({logDesc}) | {tuple(invertedSetItem)} found at {f"X = {x}" if x >= 0 else ""}{" , " if x >= 0 and y >= 0 else ""}{f"Y = {y}" if y >= 0 else ""}')
                    return True
        return False