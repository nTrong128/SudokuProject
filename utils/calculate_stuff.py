from objects.coordinate import Coord


def get_area_by_coord(coord: Coord):
    return (coord.row // 3) * 3 + (coord.col // 3)


def top_left_corner_coord(area: int) -> Coord:
    return Coord(area // 3 * 3, area % 3 * 3)


def map_to_area_index(board_coord: Coord) -> tuple[int, int]:
    area = get_area_by_coord(board_coord)
    top_left_coord = top_left_corner_coord(area)
    area_index = (board_coord.row - top_left_coord.row) * 3 + (board_coord.col - top_left_coord.col)
    return area, area_index