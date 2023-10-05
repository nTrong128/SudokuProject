import random

from objects.board import Board


def fillArea(sudoku_Board: Board):
    for area in range(0, 9):
        for cell in range(0, 9):
            i = random.randint(1, 9)
            while sudoku_Board.areas[area][cell] == 0:
                value = random.randint(1, 9)
                if value not in sudoku_Board.areas[area][::]:
                    sudoku_Board.areas[area][cell] = value

        top_left_index_Col = area * 3 // 9 * 3
        top_left_index_Row = area * 3 % 9

        counter = 0
        for i in range(top_left_index_Col, top_left_index_Col + 3):
            for j in range(top_left_index_Row, top_left_index_Row + 3):
                sudoku_Board.rows[i][j] = sudoku_Board.areas[area][counter]
                counter += 1

        counter = 0
        for i in range(top_left_index_Row, top_left_index_Row + 3):
            for j in range(top_left_index_Col, top_left_index_Col + 3):
                sudoku_Board.cols[i][j] = sudoku_Board.areas[area][counter]
                counter += 1
