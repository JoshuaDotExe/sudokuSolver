import logging

from src.app.lib.base import base

class nakedSingles:
    # Checks if only one pencil mark remains in each space
    # if true it replaces the grid space with it
    def solveNakedSingles(self: base):
        for yCoord, row in enumerate(self.marks):
            for xCoord, item in enumerate(row):
                if len(item) == 1:
                    self.grid[yCoord][xCoord] = item[0]
                    self.turnMoves += 1
                    logging.info(f"SOLVED | LONE SINGLE | Space ({xCoord},{yCoord}) is a {item[0]}")
        self.removeBasicMarks()