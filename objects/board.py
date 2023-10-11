import copy
from collections import namedtuple
from typing import Dict
import random
from itertools import count
import numpy as np

from SudokuProject.constants import SUB_GRID_SIZE
from SudokuProject.utils.calculate_stuff import map_to_area_index

GRID_SIZE = 9

class Board:
    def __init__(self, rows=None, cols=None, areas=None):
        self.fitness_evaluation = 0
        if rows is None or cols is None or areas is None:
            self.rows = {i: [[0, False] for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.cols = {i: [[0, False] for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
            self.areas = {i: [[0, False] for i in range(GRID_SIZE)] for i in range(GRID_SIZE)}
        else:
            self.rows = copy.deepcopy(rows)
            self.cols = copy.deepcopy(cols)
            self.areas = copy.deepcopy(areas)
            self.fitness_evaluation=self.fitness()
    def is_unchangeable(self, row, col):
        """"check the position is unchangeable or not"""
        return self.areas[row][col][1]
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

    def map_area_values_to_rows_cols(self, area: int) -> None:
        top_left_index_Col = area * SUB_GRID_SIZE // GRID_SIZE * SUB_GRID_SIZE
        top_left_index_Row = area * SUB_GRID_SIZE % GRID_SIZE
        """
        filling Rows in Board with values from the Areas
        """
        counter = 0
        for i in range(top_left_index_Col, top_left_index_Col + SUB_GRID_SIZE):
            for j in range(top_left_index_Row, top_left_index_Row + SUB_GRID_SIZE):
                self.rows[i][j] = self.areas[area][counter]
                counter += 1
        """
        filling Cols in Board with values from the Areas
        """
        counter = 0
        for i in range(top_left_index_Row, top_left_index_Row + SUB_GRID_SIZE):
            for j in range(top_left_index_Col, top_left_index_Col + SUB_GRID_SIZE):
                self.cols[i][j] = self.areas[area][counter]
                counter += 1
    def update_Board_by_areas(self):
        for area in range(len(self.areas)):
            self.map_area_values_to_rows_cols(area)
        self.fitness()
    def add_value_by_coord(self, row,col, value: int):# use to init Board with values
        self.rows[row][col][0] = value
        self.cols[col][row][0] = value
        self.rows[row][col][1] = True
        self.cols[col][row][1] = True
        area_index, value_index = map_to_area_index(row,col)
        self.areas[area_index][value_index][0] = value
        self.areas[area_index][value_index][1] = True
    def fitness(self):
        count_duplicate=lambda arr:len([x for x in arr if x!=0]) - len(set(x for x in arr if x!=0))
        for index in range(GRID_SIZE):
            self.fitness_evaluation+=(count_duplicate([self.rows[index][j][0] for j in range(GRID_SIZE)]) +count_duplicate([self.cols[index][j][0] for j in range(GRID_SIZE)]))
        return self.fitness_evaluation

    def fill_Board(self):
        """
        Fills the areas of the sudoku board with random values
        """
        for area in range(0, GRID_SIZE):
            number = [x for x in range(1, GRID_SIZE + 1) if x not in [self.areas[area][j][0] for j in range(GRID_SIZE)]]
            for cell in range(0, GRID_SIZE):
                if self.areas[area][cell][0] == 0:
                    value = random.choice(number)
                    self.areas[area][cell][0] = value
                    number.remove(value)
            top_left_index_Col = area * SUB_GRID_SIZE // GRID_SIZE * SUB_GRID_SIZE
            top_left_index_Row = area * SUB_GRID_SIZE % GRID_SIZE

            """
            filling Rows in Board with values from the Areas
            """
            counter = 0
            for i in range(top_left_index_Col, top_left_index_Col + SUB_GRID_SIZE):
                for j in range(top_left_index_Row, top_left_index_Row + SUB_GRID_SIZE):
                    self.rows[i][j][0] = self.areas[area][counter][0]
                    counter += 1
            """
            filling Cols in Board with values from the Areas
            """
            counter = 0
            for i in range(top_left_index_Row, top_left_index_Row + SUB_GRID_SIZE):
                for j in range(top_left_index_Col, top_left_index_Col + SUB_GRID_SIZE):
                    self.cols[i][j][0] = self.areas[area][counter][0]
                    counter += 1
        self.fitness_evaluation=self.fitness()
        return self

    def swap_update_2valid(self):
        # Find the indices of all occurrences of True in the nested list
        valid_positions = [(k, i, j) for k, sublist in self.rows.items()
                          for i, (j, val) in enumerate(sublist) if val == False]
        # Ensure that there are at least two positions with True to swap
        if len(valid_positions) < 2:
            return self.rows  # Not enough True values to swap, return the original list

        # Choose two random positions to swap
        index1, index2 = random.sample(valid_positions, 2)

        # print(index1)
        # print(index2)

        # update for rows
        self.rows[index1[0]][index1[1]], self.rows[index2[0]][index2[1]] = \
        self.rows[index2[0]][index2[1]], self.rows[index1[0]][index1[1]]
        # update for columns
        self.cols[index1[1]][index1[0]], self.cols[index2[1]][index2[0]] = \
        self.cols[index2[1]][index2[0]], self.cols[index1[1]][index1[0]]
        # update for areas
        area_index1, value_index1 = map_to_area_index(index1[0], index1[1])
        area_index2, value_index2 = map_to_area_index(index2[0], index2[1])
        self.areas[area_index1][value_index1], self.areas[area_index2][value_index2] = \
        self.areas[area_index2][value_index2], self.areas[area_index1][value_index1]
        #update fitness
        self.fitness_evaluation = self.fitness()
        #return self.areas

test=Board()
zero_values_in_row = [test.cols[8][j][0] for j in range(GRID_SIZE)]
# Print the list of 0 values in the specified row
print(zero_values_in_row)

print(test.fitness())

