from utils.read_file import read_from_file

if __name__ == "__main__":
    board = read_from_file("sudoku_file/input1.txt")
    board.print()