import unittest

from SudokuProject.objects.coordinate import Coord
from SudokuProject.utils.calculate_stuff import get_area_by_coord, top_left_corner_coord, map_to_area_index


class TestCalculateStuffFunctions(unittest.TestCase):
    def test_get_area_by_coord(self):
        self.assertEqual(get_area_by_coord(Coord(1, 2)), 0, "Should be 0")
        self.assertEqual(get_area_by_coord(Coord(0, 4)), 1, "Should be 1")
        self.assertEqual(get_area_by_coord(Coord(2, 8)), 2, "Should be 2")
        self.assertEqual(get_area_by_coord(Coord(4, 1)), 3, "Should be 3")
        self.assertEqual(get_area_by_coord(Coord(3, 3)), 4, "Should be 4")
        self.assertEqual(get_area_by_coord(Coord(4, 6)), 5, "Should be 5")
        self.assertEqual(get_area_by_coord(Coord(7, 2)), 6, "Should be 6")
        self.assertEqual(get_area_by_coord(Coord(8, 5)), 7, "Should be 7")
        self.assertEqual(get_area_by_coord(Coord(7, 8)), 8, "Should be 8")

    def test_top_left_corner_coord(self):
        self.assertEqual(top_left_corner_coord(0), Coord(0, 0), "Should be (0, 0)")
        self.assertEqual(top_left_corner_coord(1), Coord(0, 3), "Should be (0, 3)")
        self.assertEqual(top_left_corner_coord(2), Coord(0, 6), "Should be (0, 6)")
        self.assertEqual(top_left_corner_coord(3), Coord(3, 0), "Should be (3, 0)")
        self.assertEqual(top_left_corner_coord(4), Coord(3, 3), "Should be (3, 3)")
        self.assertEqual(top_left_corner_coord(5), Coord(3, 6), "Should be (3, 6)")
        self.assertEqual(top_left_corner_coord(6), Coord(6, 0), "Should be (6, 0)")
        self.assertEqual(top_left_corner_coord(7), Coord(6, 3), "Should be (6, 3)")
        self.assertEqual(top_left_corner_coord(8), Coord(6, 6), "Should be (6, 6)")

    def test_map_to_area_coord(self):
        self.assertEqual(map_to_area_index(Coord(1, 2)), (0, 5))
        self.assertEqual(map_to_area_index(Coord(0, 4)), (1, 1))
        self.assertEqual(map_to_area_index(Coord(2, 8)), (2, 8))
        self.assertEqual(map_to_area_index(Coord(4, 1)), (3, 4))
        self.assertEqual(map_to_area_index(Coord(3, 3)), (4, 0))
        self.assertEqual(map_to_area_index(Coord(4, 6)), (5, 3))
        self.assertEqual(map_to_area_index(Coord(7, 2)), (6, 5))
        self.assertEqual(map_to_area_index(Coord(8, 5)), (7, 8))
        self.assertEqual(map_to_area_index(Coord(7, 8)), (8, 5))


if __name__ == '__main__':
    unittest.main()
