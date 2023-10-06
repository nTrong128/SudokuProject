from collections import namedtuple
from typing import Dict
import random
from constants import GRID_SIZE
from objects.coordinate import Coord
from utils.calculate_stuff import map_to_area_index

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

        self.fitness_evaluation=0
        self.fixed_values: Dict[Coord, int] = {}
    

    def print(self):
        print(self.fitness_evaluation)
        print("Rows: ")
        for row in self.rows:
            print(f'{row}: {self.rows[row]}')
        print("Cols: ")
        for col in self.cols:
            print(f'{col}: {self.cols[col]}')
        print("Areas: ")
        for area in self.areas:
            print(f'{area}: {self.areas[area]}')
        print("Fixed values: ")
        for coord in self.fixed_values:
            print(f'{coord}: {self.fixed_values[coord]}')

    def add_value_by_coord(self, coord: Coord, value: int):
        self.rows[coord.row][coord.col] = value
        self.cols[coord.col][coord.row] = value
        area_index, value_index = map_to_area_index(coord)
        self.areas[area_index][value_index] = value
        self.fixed_values[coord] = value
    def fitness(self):
        count_duplicate=lambda arr:len([x for x in arr if x!=0]) - len(set(x for x in arr if x!=0))
        for index in range(GRID_SIZE):
            self.fitness_evaluation+=count_duplicate(self.rows[index]) +count_duplicate(self.cols[index])
        return self.fitness_evaluation

    def fillArea(self):
        """
        Fills the areas of the sudoku board with random values
        """
        for area in range(0, GRID_SIZE):
            number = [x for x in range(1, GRID_SIZE + 1) if x not in self.areas[area]]
            for cell in range(0, GRID_SIZE):
                if self.areas[area][cell] == 0:
                    value = random.choice(number)
                    self.areas[area][cell] = value
                    number.remove(value)
            top_left_index_Col = area * 3 // GRID_SIZE * 3
            top_left_index_Row = area * 3 % GRID_SIZE

            """
            filling Rows in Board with values from the Areas
            """
            counter = 0
            for i in range(top_left_index_Col, top_left_index_Col + 3):
                for j in range(top_left_index_Row, top_left_index_Row + 3):
                    self.rows[i][j] = self.areas[area][counter]
                    counter += 1
            """
            filling Cols in Board with values from the Areas
            """
            counter = 0
            for i in range(top_left_index_Row, top_left_index_Row + 3):
                for j in range(top_left_index_Col, top_left_index_Col + 3):
                    self.cols[i][j] = self.areas[area][counter]
                    counter += 1
        return self
