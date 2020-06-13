import unittest
import src.maze as maze

class Test(unittest.TestCase):
    #Testuje wartości otrzymane od funkcji
    def test_value(self):
        a = maze.generateGrid(13, 18, (2, 0), (0, 10))
        self.assertEqual(len(a), 13)
        self.assertEqual(len(a[0]), 18)

    def test_errors(self):
        self.assertRaises(maze.InvalidPositionError, maze.generateGrid,
                            20, 13, (0, 0), (0, 0))
        self.assertRaises(maze.InvalidDimensionsError, maze.generateGrid,
                            0, 10, (0, 2), (10, 0))
        self.assertRaises(maze.InvalidDimensionsError, maze.generateGrid,
                            32, 10, (0, 2), (10, 0))