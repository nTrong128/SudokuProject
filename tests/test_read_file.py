import unittest

from objects.board import Board
from objects.coordinate import Coord
from utils.read_file import read_from_file

unittest.TestCase.maxDiff = None


class TestReadFile(unittest.TestCase):
    def test_read_from_file(self):
        sudoku_from_file = read_from_file("input1.txt")
        sudoku_target = Board(
            rows={
                0: [0, 6, 1, 0, 0, 7, 0, 0, 3],
                1: [0, 9, 0, 0, 0, 3, 0, 0, 0],
                2: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                3: [0, 0, 8, 5, 3, 0, 0, 0, 0],
                4: [0, 0, 0, 0, 0, 0, 5, 0, 4],
                5: [0, 0, 0, 0, 0, 8, 0, 0, 0],
                6: [0, 4, 0, 0, 0, 0, 0, 0, 1],
                7: [0, 0, 0, 1, 6, 0, 8, 0, 0],
                8: [6, 0, 0, 0, 0, 0, 0, 0, 0]
            },
            cols={
                0: [0, 0, 0, 0, 0, 0, 0, 0, 6],
                1: [6, 9, 0, 0, 0, 0, 4, 0, 0],
                2: [1, 0, 0, 8, 0, 0, 0, 0, 0],
                3: [0, 0, 0, 5, 0, 0, 0, 1, 0],
                4: [0, 0, 0, 3, 0, 0, 0, 6, 0],
                5: [7, 3, 0, 0, 0, 8, 0, 0, 0],
                6: [0, 0, 0, 0, 5, 0, 0, 8, 0],
                7: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                8: [3, 0, 0, 0, 4, 0, 1, 0, 0]
            },
            areas={
                0: [0, 6, 1, 0, 9, 0, 0, 0, 0],
                1: [0, 0, 7, 0, 0, 3, 0, 0, 0],
                2: [0, 0, 3, 0, 0, 0, 0, 0, 0],
                3: [0, 0, 8, 0, 0, 0, 0, 0, 0],
                4: [5, 3, 0, 0, 0, 0, 0, 0, 8],
                5: [0, 0, 0, 5, 0, 4, 0, 0, 0],
                6: [0, 4, 0, 0, 0, 0, 6, 0, 0],
                7: [0, 0, 0, 1, 6, 0, 0, 0, 0],
                8: [0, 0, 1, 8, 0, 0, 0, 0, 0]
            },
            fixed_value={
                Coord(0, 1): 6,
                Coord(0, 2): 1,
                Coord(0, 5): 7,
                Coord(0, 8): 3,
                Coord(1, 1): 9,
                Coord(1, 5): 3,
                Coord(3, 2): 8,
                Coord(3, 3): 5,
                Coord(3, 4): 3,
                Coord(4, 6): 5,
                Coord(4, 8): 4,
                Coord(5, 5): 8,
                Coord(6, 1): 4,
                Coord(6, 8): 1,
                Coord(7, 3): 1,
                Coord(7, 4): 6,
                Coord(7, 6): 8,
                Coord(8, 0): 6
            }
        )

        self.assertDictEqual(sudoku_from_file.rows, sudoku_target.rows)
        self.assertDictEqual(sudoku_from_file.cols, sudoku_target.cols)
        self.assertDictEqual(sudoku_from_file.areas, sudoku_target.areas)
        self.assertDictEqual(sudoku_from_file.fixed_values, sudoku_target.fixed_values)


if __name__ == "__main__":
    unittest.main()
