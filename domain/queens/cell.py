from z3 import Bool

class Cell:

    def __init__(self, row, col, color, val=-1):
        self.id = Bool(f"cell_{row}_{col}")
        self.row = row
        self.col = col
        self.color = color
        self.val = val

    def update_value(self, val):
        if val not in [-1, 0, 1]:
            raise ValueError(f"Invalid cell value: {val}")
        self.val = val

    def get_color(self):
        return self.color

    def get_value_str(self):
        if self.val == -1:
            return self.color
        elif self.val == 1:
            return "Q"
        elif self.val == 0:
            return "."
        else:
            raise ValueError(f"Invalid cell value: {self.val}")

    def get_variable(self):
        return self.id