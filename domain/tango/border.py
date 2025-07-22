"""
Represents the border between two cells in a grid. Can be thre possible states: normal, equal or different.
"""
class Border:
    def __init__(self, row: int, col: int, val: int, horizontal_border: bool = False):
        self.row = row
        self.col = col
        self.val = val
        self.horizontal_border = horizontal_border

    def get_row(self) -> int:
        return self.row
    
    def get_col(self) -> int:
        return self.col

    def is_equal(self) -> bool:
        return self.val == 0
    
    def is_different(self) -> bool:
        return self.val == 1
    
    def is_horizontal(self) -> bool:
        return self.horizontal_border

    def get_value_str(self) -> str:
        char = ""
        if self.val == -1:
            char = "-" if self.horizontal_border else "|"
        elif self.val == 0:
            char = "="
        elif self.val == 1:
            char = "x"
        else:
            raise ValueError(f"Invalid border value: {self.val}")
        return char + " " if self.horizontal_border else char