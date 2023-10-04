from objects.coordinate import Coord


def get_area_index_by_coord(coord: Coord):
    return (coord.row // 3) * 3 + (coord.col // 3)


def map_to_area_coord(board_coord: Coord):
    area_index = get_area_index_by_coord(board_coord)
    top_left_coord = Coord(area_index // 3 * 3, area_index % 3 * 3)
    index = (board_coord.row - top_left_coord.row) * 3 + (board_coord.col - top_left_coord.col)
    return area_index, index
