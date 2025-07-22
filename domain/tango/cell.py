"""
Represents a cell in a grid. Can have 3 possible states: empty, sun or moon.
"""
from z3 import Bool
class Cell:

    def __init__(self, row: int, col: int, val : int):
        self.id = Bool(f"cell_{row}_{col}")
        self.row = row
        self.col = col
        self.val = val

    def update_value(self, val: int):
        if val not in [-1, 0, 1]:
            raise ValueError(f"Invalid cell value: {val}")
        self.val = val

    def is_static(self) -> bool:
        return self.val != -1

    def get_value_bool(self) -> bool:
        if self.val == 0:
            return False
        elif self.val == 1:
            return True
        elif self.val == -1:
            return None
        else:
            raise ValueError(f"Invalid cell value: {self.val}")

    def get_value_str(self) -> str:
        if self.val == -1:
            return " "
        elif self.val == 1:
            return "S"
        elif self.val == 0:
            return "M"
        else:
            raise ValueError(f"Invalid cell value: {self.val}")
        
    def get_variable(self):
        return self.id

    