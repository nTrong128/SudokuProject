import copy
import random

from constants import GRID_SIZE
from objects.board import Board
from utils.calculate_stuff import get_coord_by_area_index, top_left_corner_coord


def fill_areas(sudoku_Board: Board) -> None:
    #Fills the areas of the sudoku board with random values
    for area in range(GRID_SIZE):
        number = [x for x in range(1, GRID_SIZE + 1) if x not in sudoku_Board.areas[area]]
        for cell in range(GRID_SIZE):
            if sudoku_Board.areas[area][cell] == 0:
                value = random.choice(number)
                sudoku_Board.areas[area][cell] = value
                number.remove(value)

def update_cols_by_area(sudoku_board: Board, area: int):
    top_left_coord = top_left_corner_coord(area)

    base_counter = 0
    for col in range(top_left_coord.col, top_left_coord.col + 3):
        counter = base_counter
        for row in range(top_left_coord.row, top_left_coord.row + 3):
            sudoku_board.cols[col][row] = sudoku_board.areas[area][counter]
            counter += 3
        base_counter += 1
def update_rows_by_area(sudoku_board: Board, area: int) -> None:
    top_left_index_Col = area * 3 // GRID_SIZE * 3
    top_left_index_Row = area * 3 % GRID_SIZE
    counter = 0
    for i in range(top_left_index_Col, top_left_index_Col + 3):
        for j in range(top_left_index_Row, top_left_index_Row + 3):
            sudoku_board.rows[i][j] = sudoku_board.areas[area][counter]
            counter += 1
def map_area_values_to_rows_cols(sudoku_board: Board, area: int) -> None:
    update_rows_by_area(sudoku_board, area)
    update_cols_by_area(sudoku_board, area)

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
        board.areas = copy.deepcopy(input_board.areas)
        fill_areas(board)
        update_board_by_areas(board)
        population.append(board)
    return population


def create_one_child(parent_Board: Board, mother_Board: Board, mutation=False) -> Board:
    child_board = Board()
    for j in range(GRID_SIZE):
        child_board.areas[j] = copy.deepcopy(random.choice([parent_Board.areas[j], mother_Board.areas[j]]))
    if child_board.fitness_evaluation == 2:
        mutate_individual(child_board)
    if mutation:
        mutate_individual(child_board)
    return child_board


def create_child(population: list[Board], children_size: int, selection_rate, random_selection_rate) -> list[Board]:
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

        # child_evaluaton = []
        for i in range(children_size):
            # child_board = create_one_child(population[father_index], population[mother_index])
            if i != 1:
                child_board = create_one_child(population[father_index], population[mother_index], True)
            else:
                child_board = create_one_child(population[father_index], population[mother_index])

            update_board_by_areas(child_board)
            population.append(child_board)
            # child_evaluaton.append(child_board.fitness_evaluation)
        # if population[father_index].fitness_evaluation < min(child_evaluaton):
        population.pop(father_index)
        population.pop(mother_index)

    # return population
    return natural_selection(population, selection_rate, random_selection_rate)


def sort_population(population: list[Board]) -> list[Board]:
    return sorted(population, key=lambda x: x.fitness_evaluation, reverse=False)


def natural_selection(population: list[Board], selection_rate, random_selection_rate) -> list[Board]:
    population = sort_population(population)
    partition_size = int(len(population) * selection_rate*2)
    good_population = population[:partition_size]
    weights = [x.fitness_evaluation for x in population[partition_size:]]
    max_weights = max(weights)
    weights = [max_weights - x for x in weights ]
    random_population = random.choices(population[partition_size:], weights=weights,
                                       k=int(len(population) * random_selection_rate))
    # population = copy.deepcopy(good_population + random_population)
    population = copy.deepcopy(good_population)

    random.shuffle(population)
    return population


# def area_for_mutate(sudoku_board: Board) -> int:
#     max_area: int = 0
#     area_index: int
#     for i in range(GRID_SIZE):
#         if sudoku_board.area_ranking(i) > max_area:
#             max_area = sudoku_board.area_ranking(i)
#             area_index = i
#
#     return area_index

def mutate_area(sudoku_board: Board, area: int) -> bool:
    # area = area_for_mutate(sudoku_board)
    area_values = sudoku_board.areas[area]
    available_indices_to_swap = []

    for index, value in enumerate(area_values):
        coord = get_coord_by_area_index(area, index)
        if coord not in sudoku_board.fixed_values:
            available_indices_to_swap.append((index, coord))

    if len(available_indices_to_swap) == 0 or len(available_indices_to_swap) == 1:
        return False

    weights = [sudoku_board.calculate_duplicates_by_coord(elem[1]) for elem in available_indices_to_swap]

    pair_to_swap = random.choices(available_indices_to_swap, weights=weights, k=2)

    index_1 = pair_to_swap[0][0]
    index_2 = pair_to_swap[1][0]

    coord_1 = pair_to_swap[0][1]
    coord_2 = pair_to_swap[1][1]
    if coord_1.col != coord_2.col or coord_1.row != coord_2.row:
        area_values[index_1], area_values[index_2] = area_values[index_2], area_values[index_1]
    else:
        return False

    return True


def mutate_individual(sudoku_board: Board):
    area_to_choose = list(range(9))
    area_scores = [sudoku_board.area_ranking(area) for area in range(GRID_SIZE)]

    area_to_mutate = random.choices(area_to_choose, weights=area_scores, k=1)

    mutate_area(sudoku_board, area_to_mutate[0])



#
# listch = [1,2,3,4,5,6,7,8,9,10]
# weights = [1,2,0,2,0,0,1,1,3,1]
# for i in range(100):
#     print(random.choices(listch, weights=weights, k=1))