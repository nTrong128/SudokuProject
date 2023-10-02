from sudoku import Sudoku


def read_from_file(file_name: str):
    board = []
    with open(file_name, 'r') as file:
        for row_idx, line in enumerate(file):
            board.append([int(x) for x in line.split()])

    return Sudoku(board)