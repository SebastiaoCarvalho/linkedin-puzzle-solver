from domain.puzzle import Puzzle
from domain.zip.cell import Cell
from domain.zip.number import Number
from z3 import IntSort, BoolSort, Function

class Zip(Puzzle):
    """
    Class representing a Zip puzzle.
    """

    def __init__(self, cells: list[list[Cell]], numbers: list[Number]):
        self.cells = cells
        self.numbers = numbers
        self.reach = Function("Reach", IntSort(), IntSort(), IntSort(), IntSort(), BoolSort()) # You can reach Y from X

    def get_reach(self):
        return self.reach

    def get_cells(self):
        return self.cells
    
    def exists_number(self, row: int, col: int) -> bool:
        """
        Check if a number exists at the given cell coordinates.
        """
        return any(number.get_row() == row and number.get_col() == col for number in self.numbers)
    
    def get_number(self, row: int, col: int) -> Number | None:
        """
        Get the number at the given cell coordinates.
        """
        for number in self.numbers:
            if number.get_row() == row and number.get_col() == col:
                return number
        return None
    
    def get_numbers_sorted(self) -> list[Number]:
        """
        Get the numbers sorted by their value.
        """
        return sorted(self.numbers, key=lambda number: number.get_value())
    
    def get_first_number(self) -> Number:
        """
        Get the first number in the puzzle.
        """
        return self.numbers[0] 

    def get_last_number(self) -> Number:
        """
        Get the last number in the puzzle.
        """
        max_number = len(self.numbers)
        for number in self.numbers:
            if number.get_value() == max_number:
                return number
    
    def get_board(self):
        board_str = ""
        for row in self.cells:
            for cell in row:
                if cell.get_value_str() != "." or not self.exists_number(cell.get_row(), cell.get_col()):
                    board_str += cell.get_value_str()
                else:
                    number = self.get_number(cell.get_row(), cell.get_col())
                    board_str += number.get_value_str()
            board_str += "\n"
        return board_str.rstrip()  # Remove trailing newlinecol