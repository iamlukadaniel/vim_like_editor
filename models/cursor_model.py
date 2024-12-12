from typing import Tuple


class CursorModel:
    def __init__(self, row: int = 0, col: int = 0):
        self.row: int = row
        self.col: int = col

    def move(self, row_offset: int, col_offset: int) -> None:
        self.row += row_offset
        self.col += col_offset

    def set_position(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def get_position(self) -> Tuple[int, int]:
        return self.row, self.col
