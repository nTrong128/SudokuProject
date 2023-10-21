import time

from objects.coordinate import Coord
from sudoku_GA import sudoku_GA, mutate_individual, fill_areas, update_board_by_areas
from utils.read_file import read_from_file

if __name__ == "__main__":
    start_time = time.time()
    sudoku_board = read_from_file("default.txt")

    # fill_areas(sudoku_board)
    # update_board_by_areas(sudoku_board)

    # sudoku_board.print_matrix()
    #
    # mutate_individual(sudoku_board)

    # sudoku_board.print_matrix()

    sudoku_GA(sudoku_board)

    end_time = time.time()
    print("RUN TIME: ", round((end_time - start_time), 4), "seconds")
    # sudoku_board.update_fitness()
    # sudoku_board.print_matrix()
    # mutate_individual(sudoku_board)
    # sudoku_board.print_matrix()
