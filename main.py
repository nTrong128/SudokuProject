from sudoku_GA import create_population, create_child
from utils.read_file import read_from_file
import time

start_time = time.time()
if __name__ == "__main__":
    board = read_from_file("input1.txt")

    population_size = 500
    children_size = 4
    population = create_population(board, population_size)
    generation = 20
    selection_rate = 0.25
    random_selection_rate = 0.25
    for i in range(generation):
        create_child(population, children_size, selection_rate,random_selection_rate)
        print("Generation :", i+1)
        print("Number of individuals: ", len(population))
        min_evaluation = min(population, key=lambda x: x.fitness_evaluation)
        print("Min evaluation: ", min_evaluation.fitness_evaluation)
        if i == generation:
            min_evaluation.print_matrix()

    min_evaluation.print_matrix()

    end_time = time.time()
    print("The time of execution of above program is :",
          (end_time - start_time) * 10 ** 3, "ms")