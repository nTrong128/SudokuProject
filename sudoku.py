from constants import BOARD_SIZE, AREA_SIZE


class Sudoku:
    def __init__(self, board: list[list[int]] = None):
        if board is not None:
            self.board = board
        else:
            self.board = [[0 for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    def __repr__(self) -> str:
        res = ""
        for row_idx, row in enumerate(self.board):
            res += " ".join([str(row[i]) if (i + 1) % AREA_SIZE != 0 or (i + 1) == BOARD_SIZE else str(row[i]) + " |" for i in range(BOARD_SIZE)]) + "\n"
            if (row_idx + 1) % 3 == 0 and (row_idx + 1) != BOARD_SIZE:
                res += "---------------------\n"
        return res


