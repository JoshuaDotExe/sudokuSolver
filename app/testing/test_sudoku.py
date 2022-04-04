import unittest

from app.lib.sudoku import sudoku

class TestGrid(unittest.TestCase):
    
    def setUp(self):
        self.testEasy = sudoku.loadFromJSON("_testEasy")
        self.testMedium = sudoku.loadFromJSON("_testMedium")
        self.testHard = sudoku.loadFromJSON("_testHard")
        self.testBlank = sudoku.loadFromJSON("_testBlank")
    
    def tearDown(self):
        del self.testEasy
        del self.testMedium
        del self.testHard
        del self.testBlank
    
    def test_loadFromJSON(self):
        self.assertEqual(self.testEasy.grid, [['5', '0', '0', '0', '0', '6', '0', '0', '2'],
                                              ['0', '2', '0', '7', '0', '0', '9', '1', '0'],
                                              ['0', '0', '0', '2', '1', '8', '0', '0', '0'],
                                              ['4', '0', '0', '8', '0', '0', '0', '0', '0'],
                                              ['7', '6', '0', '0', '3', '0', '8', '9', '0'],
                                              ['3', '0', '0', '6', '0', '9', '0', '0', '7'],
                                              ['0', '0', '5', '9', '0', '0', '7', '0', '0'],
                                              ['6', '7', '3', '1', '8', '5', '2', '4', '9'],
                                              ['2', '0', '8', '0', '0', '4', '6', '0', '1']],)
        self.assertEqual(self.testMedium.grid, [['7', '8', '0', '0', '9', '2', '0', '0', '0'],
                                                ['0', '0', '0', '0', '0', '8', '4', '2', '0'],
                                                ['2', '0', '6', '0', '0', '0', '8', '0', '7'],
                                                ['0', '0', '0', '3', '5', '0', '0', '0', '4'],
                                                ['0', '0', '0', '0', '0', '0', '0', '0', '5'],
                                                ['5', '4', '3', '0', '0', '0', '9', '7', '8'],
                                                ['8', '0', '9', '0', '4', '0', '5', '0', '0'],
                                                ['6', '0', '0', '0', '0', '5', '0', '0', '0'],
                                                ['0', '1', '5', '0', '0', '3', '0', '8', '2']])
        self.assertEqual(self.testHard.grid, [['0', '3', '1', '0', '4', '0', '0', '0', '0'],
                                              ['0', '0', '0', '0', '0', '5', '0', '8', '0'],
                                              ['0', '0', '7', '0', '0', '0', '0', '0', '4'],
                                              ['9', '6', '0', '0', '0', '0', '5', '0', '1'],
                                              ['1', '0', '5', '0', '9', '0', '0', '0', '6'],
                                              ['0', '0', '0', '0', '1', '6', '0', '0', '0'],
                                              ['0', '9', '6', '0', '2', '0', '0', '0', '0'],
                                              ['0', '0', '0', '7', '5', '4', '0', '3', '9'],
                                              ['0', '0', '0', '0', '0', '9', '4', '0', '8']])
        self.assertEqual(self.testBlank.grid, [["0","0","0","0","0","0","0","0","0"],
                                               ["0","0","0","0","0","0","0","0","0"],
                                               ["0","0","0","0","0","0","0","0","0"],
                                               ["0","0","0","0","0","0","0","0","0"],
                                               ["0","0","0","0","0","0","0","0","0"],
                                               ["0","0","0","0","0","0","0","0","0"],
                                               ["0","0","0","0","0","0","0","0","0"],
                                               ["0","0","0","0","0","0","0","0","0"],
                                               ["0","0","0","0","0","0","0","0","0"]])
    
    def test_returnVerticalNeighbours(self):
        v1 = self.testEasy.verticalNeighbours(4)
        v2 = self.testEasy.verticalNeighbours(2)
        self.assertEqual(v1, ["1","3","8"])
        self.assertEqual(v2, ["5","3","8"])
        
    def test_returnHorizontalNeighbours(self):
        h1 = self.testEasy.horizontalNeighbours(1)
        h2 = self.testEasy.horizontalNeighbours(7)
        self.assertEqual(h1, ["2","7","9","1"])
        self.assertEqual(h2, ["6","7","3","1","8","5","2","4","9"])
        
    def test_returnBoxNeighbours(self):
        b1 = self.testEasy.boxNeighbours(0,0)
        b2 = self.testEasy.boxNeighbours(7,7)
        self.assertEqual(b1, ["5","2"])
        self.assertEqual(b2, ["7","2","4","9","6","1"])
        
    def test_blankPencilMarks(self):
        for row in self.testBlank.pencilMarks:
            for item in row:
                self.assertEqual(item, ['1','2','3','4','5','6','7','8','9'])
    
    def test_removePencilMarksVertical(self):
        self.testBlank.removePencilMarksVertical("9", 0)
        p1_correct = [
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']]
        ]
        self.assertEqual(self.testBlank.pencilMarks, p1_correct)
        
    def test_removePencilMarksHorizontal(self):
        self.testBlank.removePencilMarksHorizontal("9", 0)
        p1_correct = [
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']]
        ]
        for x, y in zip(self.testBlank.pencilMarks, p1_correct):
            self.assertEqual(x, y)
        
    def test_removePencilMarksBox(self):
        self.testBlank.removePencilMarksBox("9", 0, 0)
        p1_correct = [
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']]
        ]
        for x, y in zip(self.testBlank.pencilMarks, p1_correct):
            self.assertEqual(x, y)
        
    def test_removeSimplePencilMarks(self):
        self.testBlank.grid[0][0] = "9"
        p1_correct = [
            [[],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']]
        ]
        self.testBlank.removeBasicPencilMarks()
        self.assertEqual(self.testBlank.pencilMarks, p1_correct)
    
    def test_initPencilMarks(self):
        correct = [
            [[], ['1', '3', '4', '8', '9'], ['1', '4', '7', '9'], ['3', '4'], ['4', '9'], [], ['3', '4'], ['3', '7', '8'], []],
            [['8'], [], ['4', '6'], [], ['4', '5'], ['3'], [], [], ['3', '4', '5', '6', '8']],
            [['9'], ['3', '4', '9'], ['4', '6', '7', '9'], [], [], [], ['3', '4', '5'], ['3', '5', '6', '7'], ['3', '4', '5', '6']],
            [[], ['1', '5', '9'], ['1', '2', '9'], [], ['2', '5', '7'], ['1', '2', '7'], ['1', '3', '5'], ['2', '3', '5', '6'], ['3', '5', '6']],
            [[], [], ['1', '2'], ['4', '5'], [], ['1', '2'], [], [], ['4', '5']],
            [[], ['1', '5', '8'], ['1', '2'], [], ['2', '4', '5'], [], ['1', '4', '5'], ['2', '5'], []],
            [['1'], ['1', '4'], [], [], ['2', '6'], ['2', '3'], [], ['3', '8'], ['3', '8']],
            [[], [], [], [], [], [], [], [], []],
            [[], ['9'], [], ['3'], ['7'], [], [], ['3', '5'], []]
        ]
        self.assertEqual(self.testEasy.pencilMarks, correct)
    
    def test_loneSingles(self):
        correct = [
            ['5', '0', '0', '0', '0', '6', '0', '0', '2'],
            ['8', '2', '0', '7', '0', '3', '9', '1', '0'],
            ['9', '0', '0', '2', '1', '8', '0', '0', '0'],
            ['4', '0', '0', '8', '0', '0', '0', '0', '0'],
            ['7', '6', '0', '0', '3', '0', '8', '9', '0'],
            ['3', '0', '0', '6', '0', '9', '0', '0', '7'],
            ['1', '0', '5', '9', '0', '0', '7', '0', '0'],
            ['6', '7', '3', '1', '8', '5', '2', '4', '9'],
            ['2', '9', '8', '3', '7', '4', '6', '0', '1']
        ]
        self.testEasy.loneSingles()
        self.assertEqual(self.testEasy.grid, correct)
        
    def test_nakedPair(self):
        self.testBlank.pencilMarks[0][0] = ['2', '3']
        self.testBlank.pencilMarks[0][1] = ['2', '3']
        
        correct = [
            [['2', '3'],['2', '3'],['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9']],
            [['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']]
        ]
        self.testBlank.pencilNakedSet()
        self.assertEqual(self.testBlank.pencilMarks, correct)
        
    def test_nakedTriple(self):
        self.testBlank.pencilMarks[0][0] = ['1', '2', '3']
        self.testBlank.pencilMarks[0][1] = ['1', '2', '3']
        self.testBlank.pencilMarks[0][2] = ['1', '2', '3']
        
        correct = [
            [['1','2','3'],['1','2','3'],['1','2','3'],['4','5','6','7','8','9'],['4','5','6','7','8','9'],['4','5','6','7','8','9'],['4','5','6','7','8','9'],['4','5','6','7','8','9'],['4','5','6','7','8','9']],
            [['4','5','6','7','8','9'],['4','5','6','7','8','9'],['4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['4','5','6','7','8','9'],['4','5','6','7','8','9'],['4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']]
        ]
        self.testBlank.pencilNakedSet()
        self.assertEqual(self.testBlank.pencilMarks, correct)
    
    def test_NakedQuadLinear(self):
        self.testBlank.pencilMarks[0][0] = ['1', '2', '3', '4']
        self.testBlank.pencilMarks[0][1] = ['1', '2', '3', '4']
        self.testBlank.pencilMarks[0][2] = ['1', '2', '3', '4']
        self.testBlank.pencilMarks[0][3] = ['1', '2', '3', '4']
        
        correct = [
            [['1','2','3','4'],['1','2','3','4'],['1','2','3','4'],['1','2','3','4'],['5','6','7','8','9'],['5','6','7','8','9'],['5','6','7','8','9'],['5','6','7','8','9'],['5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']]
        ]
        self.testBlank.pencilNakedSet()
        self.assertEqual(self.testBlank.pencilMarks, correct)
    
    def test_NakedQuadBox(self):
        self.testBlank.pencilMarks[0][0] = ['1', '2', '3', '4']
        self.testBlank.pencilMarks[2][0] = ['1', '2', '3', '4']
        self.testBlank.pencilMarks[0][2] = ['1', '2', '3', '4']
        self.testBlank.pencilMarks[2][2] = ['1', '2', '3', '4']
        
        correct = [
            [['1','2','3','4'],['5','6','7','8','9'],['1','2','3','4'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['5','6','7','8','9'],['5','6','7','8','9'],['5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4'],['5','6','7','8','9'],['1','2','3','4'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']],
            [['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9'],['1','2','3','4','5','6','7','8','9']]
        ]
        self.testBlank.pencilNakedSet()
        self.assertEqual(self.testBlank.pencilMarks, correct)

if __name__ == "__main__":
    unittest.main()