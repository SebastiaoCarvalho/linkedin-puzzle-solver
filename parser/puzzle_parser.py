from domain.tango.tango import Tango
from domain.queens.queens import Queens
from domain.tango.cell import Cell as TangoCell
from domain.queens.cell import Cell as QueensCell
from domain.tango.border import Border

class PuzzleParser:
    """
    Utility class to parse textual representations of puzzles into their respective domain objects.
    Used for testing purposes.
    """

    def parse_tango(self, puzzle_str: str) -> Tango:
        lines = puzzle_str.splitlines()
        cells = []
        borders = []
        for i in range(len(lines)):
            # Case for cells
            if i % 2 == 0:
                row_cells = []
                row_borders = []
                for j, char in enumerate(lines[i]):
                    # Case for cells
                    if j % 2 == 0:
                        cell = self.parse_tango_cell(i // 2, j // 2, char)
                        row_cells.append(cell)
                    # Case for borders
                    else:
                        border = self.parse_tango_border(i // 2, j // 2, char, False)
                        row_borders.append(border)
                cells.append(row_cells)
                borders.append(row_borders)
            # Case for borders
            else:
                row_borders = []
                for j, char in enumerate(lines[i]):
                    # Case border
                    if j % 2 == 0:
                        border = self.parse_tango_border(i // 2, j // 2, char, True)
                        row_borders.append(border)
                    # Case empty space
                    else:
                        continue
                borders.append(row_borders)
        return Tango(cells, borders)

    def parse_tango_cell(self, row : int, col : int, char : int) -> TangoCell:
        value = -1
        if char == 'S':
            value = 0
        elif char == 'M':
            value = 1
        return TangoCell(row, col, value)
    
    def parse_tango_border(self, row : int, col : int, char : str, is_horizontal : bool) -> Border:
        value = -1
        if char == '=':
            value = 0
        elif char == 'x':
            value = 1
        return Border(row, col, value, is_horizontal)
            

    def parse_queens(self, puzzle_str: str) -> Queens:
        lines = puzzle_str.splitlines()
        cells = []
        for i in range(len(lines)):
            row_cells = []
            for j, char in enumerate(lines[i]):
                cell = QueensCell(i, j, char, -1)
                row_cells.append(cell)
            cells.append(row_cells)
        return Queens(cells)
    
    