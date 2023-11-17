import time

from objects.coordinate import Coord
from sudoku_GA import sudoku_GA
from utils.read_file import read_from_file

if __name__ == "__main__":
    start_time = time.time()
    sudoku_board = read_from_file("easy.txt")

    sudoku_GA(sudoku_board)
    end_time = time.time()
    print("RUN TIME: ", round((end_time - start_time), 4), "seconds")
