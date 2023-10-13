import time
from sudoku_GA import sudoku_GA
from utils.read_file import read_from_file
from constants import POPULATION_SIZE, CHILDREN_SIZE, SELECTION_RATE, MAX_GENERATION


def main():
    start_time = time.time()
    sudoku_board = read_from_file("default.txt")

    sudoku_GA(sudoku_board, POPULATION_SIZE, CHILDREN_SIZE, SELECTION_RATE, MAX_GENERATION, True)

    end_time = time.time()
    print("RUN TIME: ", round((end_time - start_time),4), "seconds")


if __name__ == "__main__":
    main()
