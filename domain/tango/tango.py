from domain.puzzle import Puzzle
from domain.tango.cell import Cell
from domain.tango.border import Border

class Tango(Puzzle):
    def __init__(self, cells : list[list[Cell]], borders : list[list[Border]]):
        self.cells = cells
        self.borders = borders

    def get_cells(self):
        return self.cells
    
    def get_borders(self):
        return self.borders

    def get_board(self):
        board_str = ""
        for i in range(len(self.cells)):
            # Add cells for a row and the borders between them
            for j in range(len(self.cells[i])):
                cell = self.cells[i][j].get_value_str()
                board_str += cell
                if j < len(self.cells[i]) - 1:
                    border = self.borders[i * 2][j].get_value_str()
                    board_str += border
            board_str += "\n"
            # Add borders between rows
            if i == len(self.cells) - 1:
                continue
            for j in range(len(self.borders[i * 2 + 1])):
                border = self.borders[i * 2 + 1][j].get_value_str()
                board_str += border
            board_str += "\n"
        return board_str.rstrip()