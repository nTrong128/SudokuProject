import copy
import random

from constants import GRID_SIZE
from objects.board import Board
from utils.calculate_stuff import get_coord_by_area_index, top_left_corner_coord, invert_weight_list
from utils.graph import draw_graph_scores


def fill_areas(sudoku_Board: Board) -> None:
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
    population = []
    for i in range(population_size):
        board = Board()
        board.areas = copy.deepcopy(input_board.areas)
        board.fixed_values = input_board.fixed_values
        fill_areas(board)
        update_board_by_areas(board)
        population.append(board)
    return population


def create_child(father_board: Board, mother_board: Board, mutation: bool = False) -> Board:
    child_board = Board()
    for j in range(GRID_SIZE):
        child_board.areas[j] = copy.deepcopy(random.choice([father_board.areas[j], mother_board.areas[j]]))

    child_board.fixed_values = father_board.fixed_values
    if mutation:
        mutate_individual(child_board)
        update_board_by_areas(child_board)

    if child_board.fitness_evaluation == 2:
        mutate_individual(child_board)
    return child_board


def create_children(population: list[Board], children_size: int, selection_rate):
    number_of_parents = len(population) // 2

    unvisited_parent = []
    unvisited_parent_weight = []

    new_population = []

    for x in range(len(population)):
        unvisited_parent.append(x)
        unvisited_parent_weight.append(population[x].fitness_evaluation)

    unvisited_parent_weight = invert_weight_list(unvisited_parent_weight)

    while number_of_parents > 0:
        father_index: int = 0
        mother_index: int = 0
        while father_index == mother_index:
            father_index = random.choices(unvisited_parent, weights=unvisited_parent_weight, k=1)[0]
            mother_index = random.choices(unvisited_parent, weights=unvisited_parent_weight, k=1)[0]

        for i in range(children_size):
            child_board = create_child(population[father_index], population[mother_index], True)
            update_board_by_areas(child_board)
            new_population.append(child_board)
        number_of_parents -= 1

    return natural_selection(new_population, selection_rate)


def sort_population(population: list[Board]) -> list[Board]:
    return sorted(population, key=lambda x: x.fitness_evaluation, reverse=False)

def natural_selection(population: list[Board], selection_rate) -> list[Board]:
    population = sort_population(population)
    good_population = population[:int(len(population) * selection_rate)]
    population = copy.deepcopy(good_population)
    random.shuffle(population)
    return population

def natural_selection_with_random(population: list[Board], selection_rate) -> list[Board]:
    population = sort_population(population)
    partition = int(len(population)*selection_rate/2)
    good_population = population[:partition]
    random_population = population[partition:]
    random_weights = []
    for x in range(len(random_population)):
        random_weights.append(random_population[x].fitness_evaluation)
    invert_weight_list(random_weights)
    random_population = random.choices(population[partition:], random_weights, k = partition)
    population = copy.deepcopy(good_population) + copy.deepcopy(random_population)
    random.shuffle(population)
    return population


def mutate_area(sudoku_board: Board, area: int) -> bool:
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


def sudoku_GA(sudoku_board: Board, population_size: int, children_size: int, selection_rate: float, max_generation: int,
              draw_graph: bool) -> None:
    to_restart = 15
    max_evaluation_list = []
    min_evaluation_list = []
    restart_time = 0
    population: list[Board] = create_population(sudoku_board, population_size)
    non_evolution_gen = 0
    previous_min_evaluation = 0
    loop_count = 0
    while loop_count < max_generation:
        population = create_children(population, children_size, selection_rate)
        print("Generation :", loop_count + 1)
        print("Number of individuals: ", len(population))
        min_evaluation = min(population, key=lambda x: x.fitness_evaluation)
        if loop_count == 0:
            previous_min_evaluation = min_evaluation.fitness_evaluation
        if min_evaluation.fitness_evaluation >= previous_min_evaluation:
            non_evolution_gen += 1
        else:
            previous_min_evaluation = min_evaluation.fitness_evaluation
            non_evolution_gen = 0

        max_evaluation = max(population, key=lambda x: x.fitness_evaluation)

        print("Max evaluation: ", max_evaluation.fitness_evaluation)
        max_evaluation_list.append(max_evaluation.fitness_evaluation)

        print("Min evaluation: ", min_evaluation.fitness_evaluation)
        min_evaluation_list.append(min_evaluation.fitness_evaluation)
        loop_count += 1
        if min_evaluation.fitness_evaluation == 0:
            print("\n\nRESTART TIME: ", restart_time)
            print("SOLUTION FOUND: ")
            min_evaluation.print_matrix()
            break
        if restart_time > 10:
            print("No solution found after 10 restarts")
            break
        if non_evolution_gen >= to_restart:
            print("No solution found at generation:", loop_count, ". Restart process.")
            loop_count = 0
            restart_time += 1
            population = create_population(sudoku_board, population_size)
            non_evolution_gen = 0

    if draw_graph:
        draw_graph_scores(min_evaluation_list, max_evaluation_list)
