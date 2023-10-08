import copy
import random

from constants import GRID_SIZE
from objects.board import Board
from utils.calculate_stuff import get_coord_by_area_index, top_left_corner_coord


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


def update_rows_cols_by_area(sudoku_board: Board, area: int) -> None:
    update_rows_by_area(sudoku_board, area)
    update_cols_by_area(sudoku_board, area)


def update_rows_by_area(sudoku_board: Board, area: int):
    top_left_coord = top_left_corner_coord(area)

    counter = 0
    for row in range(top_left_coord.row, top_left_coord.row + 3):
        for col in range(top_left_coord.col, top_left_coord.col + 3):
            sudoku_board.rows[row][col] = sudoku_board.areas[area][counter]
            counter += 1


def update_cols_by_area(sudoku_board: Board, area: int):
    top_left_coord = top_left_corner_coord(area)

    base_counter = 0
    for col in range(top_left_coord.col, top_left_coord.col + 3):
        counter = base_counter
        for row in range(top_left_coord.row, top_left_coord.row + 3):
            sudoku_board.cols[col][row] = sudoku_board.areas[area][counter]
            counter += 3
        base_counter += 1


def update_board_by_areas(sudoku_board: Board):
    for area in range(GRID_SIZE):
        update_rows_cols_by_area(sudoku_board, area)
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


def create_one_child(parent_Board: Board, mother_Board: Board, mutation=False) -> Board:
    child_board = Board()
    for j in range(GRID_SIZE):
        child_board.areas[j] = copy.deepcopy(random.choice([parent_Board.areas[j], mother_Board.areas[j]]))
    if mutation:
        mutate_individual(child_board)
    update_board_by_areas(child_board)

    return child_board


def create_child(population: list[Board], children_size: int, selection_rate, random_selection_rate):
    unvisited_parent = []
    for x in range(len(population)):
        unvisited_parent.append(x)

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
                mutate_individual(child_board)
            update_board_by_areas(child_board)
            population.append(child_board)

        population.pop(father_index)
        population.pop(mother_index)

    # return population
    return natural_selection(population, selection_rate, random_selection_rate)


def sort_population(population: list[Board]):
    return sorted(population, key=lambda x: x.fitness_evaluation, reverse=False)


def natural_selection(population: list[Board], selection_rate, random_selection_rate) -> list[Board]:
    population = sort_population(population)
    partition_size = int(len(population) * selection_rate)
    good_population = population[:partition_size]

    random_population = random.choices(population[partition_size:], None,
                                       k=int(len(population) * random_selection_rate))
    population = copy.deepcopy(good_population + random_population)
    random.shuffle(population)
    return population


def mutate_area(sudoku_board: Board, area: int) -> bool:
    area_values = sudoku_board.areas[area]
    available_indices_to_swap = []

    for index, value in enumerate(area_values):
        coord = get_coord_by_area_index(area, index)
        if coord not in sudoku_board.fixed_values:
            available_indices_to_swap.append((index, coord))

    if len(available_indices_to_swap) == 0:
        return False

    weights = [sudoku_board.calculate_duplicates_by_coord(elem[1]) for elem in available_indices_to_swap]

    pair_to_swap = random.choices(available_indices_to_swap, weights=weights, k=2)

    index_1 = pair_to_swap[0][0]
    index_2 = pair_to_swap[1][0]

    area_values[index_1], area_values[index_2] = area_values[index_2], area_values[index_1]

    return True


def mutate_individual(sudoku_board: Board):
    area_to_choose = list(range(9))
    area_scores = [sudoku_board.area_ranking(area) for area in range(GRID_SIZE)]

    area_to_mutate = random.choices(area_to_choose, weights=area_scores, k=1)

    mutate_area(sudoku_board, area_to_mutate[0])
