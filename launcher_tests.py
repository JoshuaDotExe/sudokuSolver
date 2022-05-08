import unittest
from testing.test_grid import TestGrid
from testing.test_marks import TestMarks
from testing.test_methods import TestMethods

testClasses = [TestGrid, TestMarks, TestMethods]
loadedTests = list()

for item in testClasses:
    testSuite = unittest.TestLoader().loadTestsFromTestCase(item)
    loadedTests.append(testSuite)

fullSuite = unittest.TestSuite(loadedTests)

unittest.TextTestRunner(verbosity=2).run(fullSuite)