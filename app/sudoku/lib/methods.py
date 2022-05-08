import unittest

from app.sudoku.game import sudoku

class TestMethod(unittest.TestCase):
    
    def setUp(self):
        self.testEasy = sudoku("_testEasy")
        self.testMedium = sudoku("_testMedium")
        self.testHard = sudoku("_testHard")
        self.testBlank = sudoku("_testBlank")
    
    def tearDown(self):
        del self.testEasy
        del self.testMedium
        del self.testHard
        del self.testBlank