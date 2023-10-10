from collections import namedtuple
from typing import Dict

from constants import GRID_SIZE
from objects.coordinate import Coord
from utils.calculate_stuff import map_to_area_index, get_coord_by_area_index


class Board:
    def __init__(self, rows=None, cols=None, areas=None, fixed_value=None):
        if rows is None or cols is None or areas is None or fixed_value is None:

            self.rows = {i: [0 for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.cols = {i: [0 for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.areas = {i: [0 for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.fixed_values: Dict[Coord, int] = {}
        else:
            self.rows = rows
            self.cols = cols
            self.areas = areas
            self.fixed_values = fixed_value

        self.fitness_evaluation = 0
        self.fixed_values: Dict[Coord, int] = {}

    def print(self):
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

    def print_area(self):
        print("Areas: ")
        for area in self.areas:
            print(f'{area}: {self.areas[area]}')

    def print_matrix(self):
        for row in range(GRID_SIZE):
            for cell in range(GRID_SIZE):
                print(f'{self.rows[row][cell]}', end=' ')
                if cell == 2 or cell == 5:
                    print(" | ", end=' ')
                if cell == 8:
                    print()
            if row == 2 or row == 5:
                print("-------|---------|--------")
        print("Evaluation: ",self.fitness_evaluation)

    def add_value_by_coord(self, coord: Coord, value: int):
        self.rows[coord.row][coord.col] = value
        self.cols[coord.col][coord.row] = value
        area_index, value_index = map_to_area_index(coord)
        self.areas[area_index][value_index] = value
        self.fixed_values[coord] = value

    def update_fitness(self):
        count_duplicate = lambda arr: len(arr) - len(set(arr))
        fitness_values = 0
        for index in range(GRID_SIZE):
            fitness_values += count_duplicate(self.rows[index]) + count_duplicate(self.cols[index])
        self.fitness_evaluation = fitness_values

    def get_value_by_coord(self, coord):
        return self.rows[coord.row][coord.col]

    def calculate_duplicates_by_coord(self, coord: Coord):
        coord_value = self.get_value_by_coord(coord)

        count_duplicates = self.rows[coord.row].count(coord_value) + self.cols[coord.col].count(coord_value)
        return count_duplicates

    def area_ranking(self, area: int):
        area_values = self.areas[area]
        coords = [get_coord_by_area_index(area, area_index) for area_index in range(len(area_values))]

        return sum([self.calculate_duplicates_by_coord(coord) for coord in coords])
