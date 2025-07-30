from z3 import Int

class Cell:
    """
    Represents a cell in a grid. 
    Can be left-to-right, right-to-left, top-to-bottom, bottom-to-top or empty.
    """
    
    def __init__(self, row: int, col: int, val: int):
        self.row = row
        self.col = col
        self.val = val
        self.id = Int(f"cell_{row}_{col}")

    def update_value(self, val: int):
        if val not in [-1, 0, 1]:
            raise ValueError(f"Invalid cell value: {val}")
        self.val = val

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.col

    def get_value_str(self) -> str:
        if self.val == -1:
            return "."
        elif self.val == 0:
            return "L"
        elif self.val == 1:
            return "R"
        elif self.val == 2:
            return "U"
        elif self.val == 3:
            return "D"