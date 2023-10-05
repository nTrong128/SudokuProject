from dataclasses import dataclass


@dataclass
class Coord:
    row: int
    col: int

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return f'({self.row}, {self.col})'
