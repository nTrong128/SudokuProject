from objects.board import Board
from sudoku_GA import create_population, create_child, create_one_child
from utils.read_file import read_from_file
import time

start_time = time.time()
if __name__ == "__main__":
    board = read_from_file("input1.txt")

    population_size = 1000
    children_size = 4
    population: list[Board] = create_population(board, population_size)
    max_generation = 250
    selection_rate = 0.25
    random_selection_rate = 0.25
    min_evaluation = Board()
    for i in range(max_generation):
        population = create_child(population, children_size, selection_rate,random_selection_rate)
        print("Generation :", i+1)
        print("Number of individuals: ", len(population))
        min_evaluation = min(population, key=lambda x: x.fitness_evaluation)
        print("Min evaluation: ", min_evaluation.fitness_evaluation)
        if min_evaluation.fitness_evaluation == 0:
            print("Solved")
            min_evaluation.print_matrix()
            break

    # min_evaluation.print_matrix()

    # population = create_population(board, 2)
    # population[0].print_matrix()
    # population[1].print_matrix()
    # child_Board = create_one_child(population[0], population[1], True)
    # child_Board.print_matrix()
    end_time = time.time()
    print("The time of execution of above program is :",
          (end_time - start_time) * 10 ** 3, "ms")