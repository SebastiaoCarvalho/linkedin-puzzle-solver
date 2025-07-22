from domain.puzzle import Puzzle
from domain.queens.cell import Cell

class Queens(Puzzle):

    def __init__(self, cells: list[list[Cell]]):
        self.cells = cells

    def get_cells(self):
        return self.cells
    
    def get_board(self) -> str:
        board_str = ""
        for row in self.cells:
            for cell in row:
                board_str += cell.get_value_str()
            board_str += "\n"
        return board_str.rstrip()