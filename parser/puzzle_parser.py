from domain.tango.tango import Tango
from domain.tango.cell import Cell
from domain.tango.border import Border

class PuzzleParser:
    
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

    def parse_tango_cell(self, row : int, col : int, char : int) -> Cell:
        value = -1
        if char == 'S':
            value = 0
        elif char == 'M':
            value = 1
        return Cell(row, col, value)
    
    def parse_tango_border(self, row : int, col : int, char : str, is_horizontal : bool) -> Border:
        value = -1
        if char == '=':
            value = 0
        elif char == 'x':
            value = 1
        return Border(row, col, value, is_horizontal)
            
    