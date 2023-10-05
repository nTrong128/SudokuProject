from collections import namedtuple
from typing import Dict

from constants import GRID_SIZE

Coord = namedtuple('coord', ['row', 'col'])


class Board:
    def __init__(self, rows=None, cols=None, areas=None):
        if rows is None or cols is None or areas is None:
            self.rows = {i: [0 for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.cols = {i: [0 for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.areas = {i: [0 for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
        else:
            self.rows = rows
            self.rows = cols
            self.areas = areas

        self.fixed_values: Dict[Coord, int] = {}
    
    def print(self):
        print("Rows: ")
        print(self.rows)
        print("Cols: ")
        print(self.cols)
        print("Areas: ")
        print(self.areas)
