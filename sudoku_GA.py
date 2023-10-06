import random

from objects.board import Board


def fillArea(sudoku_Board: Board) -> None:

    """
    Fills the areas of the sudoku board with random values
    """
    for area in range(0, 9):
        number = [x for x in range(1, 10) if x not in sudoku_Board.areas[area]]
        for cell in range(0, 9):
            if sudoku_Board.areas[area][cell] == 0:
                value = random.choice(number)
                sudoku_Board.areas[area][cell] = value
                number.remove(value)

        top_left_index_Col = area * 3 // 9 * 3
        top_left_index_Row = area * 3 % 9

        """
        filling Rows in Board with values from the Areas
        """
        counter = 0
        for i in range(top_left_index_Col, top_left_index_Col + 3):
            for j in range(top_left_index_Row, top_left_index_Row + 3):
                sudoku_Board.rows[i][j] = sudoku_Board.areas[area][counter]
                counter += 1
        """
        filling Cols in Board with values from the Areas
        """
        counter = 0
        for i in range(top_left_index_Row, top_left_index_Row + 3):
            for j in range(top_left_index_Col, top_left_index_Col + 3):
                sudoku_Board.cols[i][j] = sudoku_Board.areas[area][counter]
                counter += 1