import copy
import random

from constants import GRID_SIZE
from objects.board import Board


def fill_areas(sudoku_Board: Board) -> None:
    """
    Fills the areas of the sudoku board with random values
    """
    for area in range(GRID_SIZE):
        number = [x for x in range(1, GRID_SIZE + 1) if x not in sudoku_Board.areas[area]]
        for cell in range(GRID_SIZE):
            if sudoku_Board.areas[area][cell] == 0:
                value = random.choice(number)
                sudoku_Board.areas[area][cell] = value
                number.remove(value)

def fill_from_areas(sudoku_Board: Board)->None:
    for area in range(GRID_SIZE):

        top_left_index_Col = area * 3 // GRID_SIZE * 3
        top_left_index_Row = area * 3 % GRID_SIZE
        """
        filling Rows in Board with values from the Areas
        """
        counter = 0
        for i in range(top_left_index_Col, top_left_index_Col + 3):
            for j in range(top_left_index_Row, top_left_index_Row + 3):
                sudoku_Board.rows[i][j] = sudoku_Board.areas[area][counter]
                counter += 1
        """
        filling Cols in Board with values from the Areas
        """
        counter = 0
        for i in range(top_left_index_Row, top_left_index_Row + 3):
            for j in range(top_left_index_Col, top_left_index_Col + 3):
                sudoku_Board.cols[i][j] = sudoku_Board.areas[area][counter]
                counter += 1
def create_population(input_board: Board, population_size: int) -> list[Board]:
    """
    Creates a population of sudoku boards with random values
    """
    population = [Board() for _ in range(population_size)]
    for i in range(population_size):
        population[i].rows = copy.deepcopy(input_board.rows)
        population[i].cols = copy.deepcopy(input_board.cols)
        population[i].areas = copy.deepcopy(input_board.areas)
        fill_areas(population[i])
        fill_from_areas(population[i])
    return population

def create_child(population: list[Board])->(Board, int, int):
    father_index:int = 0
    mother_index :int = 0
    while(father_index == mother_index):
        father_index = random.randint(0, len(population))
        mother_index = random.randint(0, len(population))
    child_board = Board()
    for i in range(GRID_SIZE):
        child_board.areas[i] = copy.deepcopy(population[random.choice([father_index, mother_index])].areas[i])
    fill_from_areas(child_board)
    return child_board, father_index, mother_index