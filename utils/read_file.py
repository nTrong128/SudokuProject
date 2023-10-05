from objects.board import Board
from objects.coordinate import Coord

import os


def read_from_file(file_name: str):
    relative_path = os.path.join('..', 'samples', file_name)
    absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))

    board = Board()
    with open(absolute_path, "r") as file:
        for row, line in enumerate(file):
            curr_row = [int(x) for x in line.split()]
            for col, value in enumerate(curr_row):
                coord = Coord(row, col)
                if value != 0:
                    board.add_value_by_coord(coord, value)
    return board
