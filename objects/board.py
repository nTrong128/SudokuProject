from typing import Dict
import random
from constants import GRID_SIZE
from objects.coordinate import Coord
from utils.tools import map_to_area_index, get_coord_by_area_index
from utils.tools import get_coord_by_area_index, top_left_corner_coord, calculate_weights

class Board:
    def __init__(self, rows=None, cols=None, areas=None, fixed_value=None):
        if rows is None or cols is None or areas is None or fixed_value is None:

            self.rows = {i: [0 for _ in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.cols = {i: [0 for _ in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.areas = {i: [0 for _ in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.fixed_values: Dict[Coord, int] = {}
        else:
            self.rows = rows
            self.cols = cols
            self.areas = areas
            self.fixed_values = fixed_value

        self.fitness_evaluation = 0
    def print_debugging_info(self):
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

    def print_areas(self):
        print("Areas: ")
        for area in self.areas:
            print(f'{area}: {self.areas[area]}')

    def display(self):
        for row in range(GRID_SIZE):
            for cell in range(GRID_SIZE):
                print(f'{self.rows[row][cell]}', end=' ')
                if cell == 2 or cell == 5:
                    print(" | ", end=' ')
                if cell == 8:
                    print()
            if row == 2 or row == 5:
                print("-------|---------|--------")
        print("Evaluation: ", self.fitness_evaluation)

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

        count_duplicates = self.rows[coord.row].count(coord_value) - 1 + self.cols[coord.col].count(coord_value) - 1
        return count_duplicates

    def area_ranking(self, area: int):
        area_values = self.areas[area]
        coords = [get_coord_by_area_index(area, area_index) for area_index in range(len(area_values))]

        return sum([self.calculate_duplicates_by_coord(coord) for coord in coords])

    def fill_areas(self) -> None:
        for area in range(GRID_SIZE):
            number = [x for x in range(1, GRID_SIZE + 1) if x not in self.areas[area]]
            for cell in range(GRID_SIZE):
                if self.areas[area][cell] == 0:
                    value = random.choice(number)
                    self.areas[area][cell] = value
                    number.remove(value)

    def update_cols_by_area(self, area: int):
        top_left_coord = top_left_corner_coord(area)

        base_counter = 0
        for col in range(top_left_coord.col, top_left_coord.col + 3):
            counter = base_counter
            for row in range(top_left_coord.row, top_left_coord.row + 3):
                self.cols[col][row] = self.areas[area][counter]
                counter += 3
            base_counter += 1

    def update_rows_by_area(self, area: int) -> None:
        top_left_index_Col = area * 3 // GRID_SIZE * 3
        top_left_index_Row = area * 3 % GRID_SIZE
        counter = 0
        for i in range(top_left_index_Col, top_left_index_Col + 3):
            for j in range(top_left_index_Row, top_left_index_Row + 3):
                self.rows[i][j] = self.areas[area][counter]
                counter += 1

    def map_area_values_to_rows_cols(self, area: int) -> None:
        self.update_rows_by_area(area)
        self.update_cols_by_area(area)

        self.update_fitness()

    def update_board_by_areas(self):
        for area in range(GRID_SIZE):
            self.map_area_values_to_rows_cols( area)
