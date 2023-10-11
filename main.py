from SudokuProject.objects.board import Board
from SudokuProject.sudoku_GA import *
from SudokuProject.utils.read_file import read_from_file

if __name__ == "__main__":
    board = read_from_file("sudoku_file/input1.txt")
    board.print()
# board.swap_update_2valid()
# print('------------------------------------------')
# board.print()

population=createPopulation(board,2)
population=ranking_poppulation(population)
count=0
for i in population:
    count+=1
    print(i.print())
print(f'num_of_generation: {count}')