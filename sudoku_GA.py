import copy
import random

from constants import GRID_SIZE
from objects.board import Board
from utils.calculate_stuff import get_coord_by_area_index


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
    update_board_by_areas(sudoku_Board)





def map_area_values_to_rows_cols(sudoku_Board: Board, area: int) -> None:
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

def update_board_by_areas(sudoku_board: Board):
    for area in range(GRID_SIZE):
        map_area_values_to_rows_cols(sudoku_board, area)
    sudoku_board.update_fitness()

def create_population(input_board: Board, population_size: int) -> list[Board]:
    """
    Creates a population of sudoku boards with random values
    """
    population = []
    for i in range(population_size):
        board = Board()
        board.rows = copy.deepcopy(input_board.rows)
        board.cols = copy.deepcopy(input_board.cols)
        board.areas = copy.deepcopy(input_board.areas)
        fill_areas(board)
        population.append(board)
    return population
def create_one_child(parent_Board: Board, mother_Board: Board, mutation = False)->Board:
    child_board = Board()
    for j in range(GRID_SIZE):
        child_board.areas[j] = copy.deepcopy(random.choice([parent_Board.areas[j], mother_Board.areas[j]]))
    if mutation:
        mutate_area(child_board, random.randint(0, 8))
    update_board_by_areas(child_board)

    return child_board

def create_child(population: list[Board], children_size: int, selection_rate, random_selection_rate):

    population = copy.deepcopy(population[:int(len(population) * selection_rate)])
    unvisited_parent = [x for x in range(len(population))]

    while len(unvisited_parent) > 1:
        father_index: int = 0
        mother_index: int = 0
        while father_index == mother_index:
            father_index = random.choice(unvisited_parent)
            mother_index = random.choice(unvisited_parent)
        unvisited_parent.remove(father_index)
        unvisited_parent.remove(mother_index)

        for i in range(children_size):
            child_board = create_one_child(population[father_index], population[mother_index])
            if i == 1 or i == 2:
                mutate_area(child_board,random.randint(0, 8))
            update_board_by_areas(child_board)
            population.append(child_board)

        population.pop(father_index)
        population.pop(mother_index)

    return natural_selection(population, selection_rate, random_selection_rate)

def sort_population(population: list[Board]):
    return sorted(population, key=lambda x: x.fitness_evaluation, reverse=False)


def natural_selection(population: list[Board], selection_rate, random_selection_rate) -> list[Board]:
    population = sort_population(population)
    partition_size = int(len(population) * selection_rate)
    good_population = copy.deepcopy(population[partition_size:])

    random_population = random.choices(population[partition_size:], None,
                                       k=int(len(population) * random_selection_rate))
    return random.shuffle(good_population + random_population)


def mutate_area(sudoku_board: Board, area: int):
    area_values = sudoku_board.areas[area]
    available_indices_to_swap = []

    for index, value in enumerate(area_values):
        coord = get_coord_by_area_index(area, index)
        if coord not in sudoku_board.fixed_values:
            available_indices_to_swap.append(index)

    pair_to_swap = random.choices(available_indices_to_swap, k=2)

    index_1 = pair_to_swap[0]
    index_2 = pair_to_swap[1]

    area_values[index_1], area_values[index_2] = area_values[index_2], area_values[index_1]

    map_area_values_to_rows_cols(sudoku_board, area)
    # print("Mutate Area: ", area, "index_1: ",index_1, "index_2: ", index_2)