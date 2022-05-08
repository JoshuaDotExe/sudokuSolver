import unittest
from testing.test_grid import TestGrid
from testing.test_marks import TestMarks
from testing.test_methods import TestMethods

testClasses = [TestGrid, TestMarks, TestMethods]
testSuites = list()

for testClass in testClasses:
    testSuite = unittest.TestLoader().loadTestsFromTestCase(testClass)
    testSuites.append(testSuite)
