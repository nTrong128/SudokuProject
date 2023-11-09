import copy
import random

from constants import GRID_SIZE, POPULATION_SIZE, CHILDREN_SIZE, SELECTION_RATE, MAX_GENERATION, TO_RESTART
from objects.board import Board
from utils.tools import get_coord_by_area_index, top_left_corner_coord, calculate_weights
from utils.graph import draw_graph_scores





def create_population(input_board: Board, population_size: int) -> list[Board]:
    population = []
    for i in range(population_size):
        board = Board()
        board.areas = copy.deepcopy(input_board.areas)
        board.fixed_values = input_board.fixed_values
        board.fill_areas()
        board.update_board_by_areas()
        population.append(board)
    return population


def create_child(
        father_board: Board,
        mother_board: Board,
        mutation: bool = False
) -> Board:
    child_board = Board()
    for j in range(GRID_SIZE):
        child_board.areas[j] = copy.deepcopy(random.choice([father_board.areas[j], mother_board.areas[j]]))

    child_board.fixed_values = father_board.fixed_values

    if mutation:
        mutate_individual(child_board)

    child_board.update_board_by_areas()

    child_board.fixed_values = father_board.fixed_values

    return child_board


def create_children(
        population: list[Board],
        children_size: int,
        selection_rate: float
) -> list[Board]:
    number_of_parents = len(population) // 2

    unvisited_parent = [x for x in range(len(population))]

    unvisited_parent_weight = calculate_weights(
        iterable_list=unvisited_parent,
        func=lambda index: population[index].fitness_evaluation,
        invert=True
    )

    new_population = []

    while number_of_parents > 0:
        father_index: int = 0
        mother_index: int = 0
        while father_index == mother_index:
            father_index = random.choices(unvisited_parent, weights=unvisited_parent_weight, k=1)[0]
            mother_index = random.choices(unvisited_parent, weights=unvisited_parent_weight, k=1)[0]

        for i in range(children_size):
            child_board = create_child(population[father_index], population[mother_index], True)
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
    partition = int(len(population) * selection_rate / 2)

    good_population = population[:partition]
    remaining_population = population[partition:]

    # random_weights = []
    # for x in range(len(random_population)):
    #     random_weights.append(random_population[x].fitness_evaluation)
    # invert_weight_list(random_weights)

    remaining_weights = calculate_weights(
        iterable_list=remaining_population,
        func=lambda x: x.fitness_evaluation,
        invert=True
    )

    random_population = random.choices(remaining_population, remaining_weights, k=partition)
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

    weights = calculate_weights(
        iterable_list=available_indices_to_swap,
        func=lambda indices: sudoku_board.calculate_duplicates_by_coord(indices[1]),
    )

    pair_to_swap = random.choices(available_indices_to_swap, weights=weights, k=2)

    index_1 = pair_to_swap[0][0]
    index_2 = pair_to_swap[1][0]

    area_values[index_1], area_values[index_2] = area_values[index_2], area_values[index_1]

    return True


def mutate_individual(sudoku_board: Board):
    area_to_choose = list(range(9))

    area_weights = calculate_weights(
        iterable_list=area_to_choose,
        func=lambda area: sudoku_board.area_ranking(area),
        excluding_weights=[0, 1]
    )

    area_to_mutate = random.choices(area_to_choose, weights=area_weights, k=1)[0]

    mutate_area(sudoku_board, area_to_mutate)

    sudoku_board.map_area_values_to_rows_cols(area_to_mutate)


def sudoku_GA(
        sudoku_board: Board,
        population_size: int = POPULATION_SIZE,
        children_size: int = CHILDREN_SIZE,
        selection_rate: int = SELECTION_RATE,
        max_generation: int = MAX_GENERATION,
        to_restart: int = TO_RESTART,
        draw_graph: bool = True
) -> None:
    restart_time = 0
    non_evolution_gen = 0
    previous_min_evaluation = 0
    loop_count = 0

    population: list[Board] = create_population(sudoku_board, population_size)
    max_evaluation_list = []
    min_evaluation_list = []

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
            min_evaluation.print_debugging_info()
            break

        if restart_time > 10:
            print("No solution found after 10 restarts")
            break

        if non_evolution_gen >= to_restart:
            min_evaluation.display()
            print("No solution found at generation:", loop_count, ". Restart process.")
            loop_count = 0
            restart_time += 1
            population = create_population(sudoku_board, population_size)
            non_evolution_gen = 0

    if draw_graph:
        draw_graph_scores(min_evaluation_list, max_evaluation_list)
