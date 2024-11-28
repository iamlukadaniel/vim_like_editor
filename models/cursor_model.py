

class CursorModel:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def move(self, row_offset: int, col_offset: int):
        self.row += row_offset
        self.col += col_offset

    def set_position(self, row: int, col: int):
        self.row = row
        self.col = col

    def get_position(self):
        return self.row, self.col