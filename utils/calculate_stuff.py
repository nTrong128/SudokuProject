
from SudokuProject.constants import SUB_GRID_SIZE


def get_area_by_coord(row,col):
    return (row // 3) * 3 + (col // 3)

def top_left_corner_coord(area: int) -> list:
    return [area // SUB_GRID_SIZE * SUB_GRID_SIZE, area % SUB_GRID_SIZE * SUB_GRID_SIZE]

def map_to_area_index(row,col) -> tuple[int, int]:
    area = get_area_by_coord(row,col)
    top_left_coord = top_left_corner_coord(area)
    area_index = (row - top_left_coord[0]) * 3 + (col - top_left_coord[1])
    return area, area_index
