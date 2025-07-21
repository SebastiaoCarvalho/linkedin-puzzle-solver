"""
Represents a cell in a grid. Can have 3 possible states: empty, sun or moon.
"""
from z3 import Int
class Cell:

    def __init__(self, row: int, col: int, val : int):
        self.id = Int(f"cell_{row}_{col}")
        self.row = row
        self.col = col
        self.val = val

    def get_value_str(self) -> str:
        if self.val == -1:
            return " "
        elif self.val == 0:
            return "S"
        elif self.val == 1:
            return "M"
        else:
            raise ValueError(f"Invalid cell value: {self.val}")
        
    def get_variable(self):
        return self.id

    