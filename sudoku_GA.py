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


def fill_area_to_rowcol(sudoku_Board: Board) -> None:
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
    sudoku_Board.fitness()


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
        fill_area_to_rowcol(population[i])
    return population


def create_child(population: list[Board], population_size: int, children_size: int):
    population_size = len(population)
    undiscovered_parent = [x for x in range(population_size)]
    while len(undiscovered_parent) > 1:
        father_index: int = 0
        mother_index: int = 0
        while father_index == mother_index:
            father_index = random.choice(undiscovered_parent)
            mother_index = random.choice(undiscovered_parent)
        undiscovered_parent.remove(father_index)
        undiscovered_parent.remove(mother_index)

        for i in range(children_size):
            child_board = Board()
            for j in range(GRID_SIZE):
                child_board.areas[j] = copy.deepcopy(population[random.choice([father_index, mother_index])].areas[j])
            fill_area_to_rowcol(child_board)
            population.append(child_board)
            population_size += 1

            if population[father_index].fitness_evaluation > child_board.fitness_evaluation:
                population.pop(father_index)
                population_size -= 1

            if population[mother_index].fitness_evaluation > child_board.fitness_evaluation:
                population.pop(mother_index)
                population_size -= 1

    natural_selection(population)
def sort_population(population: list[Board]):
    return sorted(population, key=lambda x: x.fitness_evaluation, reverse=False)


def natural_selection(population: list[Board]) -> list[Board]:
    population = sort_population(population)
    divider = int(len(population)/4)
    good_population = population[:divider]
    random_population: list[Board]


    population =  copy.deepcopy(good_population)