import unittest
import logging

from app.sudoku.game import sudoku

class TestGrid(unittest.TestCase):
    
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.testEasy = sudoku("_testEasy")
        self.testMedium = sudoku("_testMedium")
        self.testHard = sudoku("_testHard")
        self.testBlank = sudoku("_testBlank")
    
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
        self.assertEqual(self.testBlank.grid, [['0','0','0','0','0','0','0','0','0'],
                                               ['0','0','0','0','0','0','0','0','0'],
                                               ['0','0','0','0','0','0','0','0','0'],
                                               ['0','0','0','0','0','0','0','0','0'],
                                               ['0','0','0','0','0','0','0','0','0'],
                                               ['0','0','0','0','0','0','0','0','0'],
                                               ['0','0','0','0','0','0','0','0','0'],
                                               ['0','0','0','0','0','0','0','0','0'],
                                               ['0','0','0','0','0','0','0','0','0'],])
        
    def test_returnVerticalNeighbours(self):
        v1 = self.testEasy.verticalNeighbours(4)
        v2 = self.testEasy.verticalNeighbours(2)
        self.assertEqual(v1, ['0', '0', '1', '0', '3', '0', '0', '8', '0'])
        self.assertEqual(v2, ['0', '0', '0', '0', '0', '0', '5', '3', '8'])
        
    def test_returnHorizontalNeighbours(self):
        h1 = self.testEasy.horizontalNeighbours(1)
        h2 = self.testEasy.horizontalNeighbours(7)
        self.assertEqual(h1, ['0', '2', '0', '7', '0', '0', '9', '1', '0'])
        self.assertEqual(h2, ['6','7','3','1','8','5','2','4','9'])
        
    def test_returnBoxNeighbours(self):
        b1 = self.testEasy.boxNeighbours(0,0)
        b2 = self.testEasy.boxNeighbours(7,7)
        self.assertEqual(b1, ['5', '0', '0', '0', '2', '0', '0', '0', '0'])
        self.assertEqual(b2, ['7', '0', '0', '2', '4', '9', '6', '0', '1'])

if __name__ == "__main__":
    unittest.main()
    