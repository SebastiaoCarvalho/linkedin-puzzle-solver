from encoding.encoder import Encoder
from z3 import Solver
from domain.tango.tango import Tango

"""
Borders with equal ensure the cells on either side have the same value.
Borders with different ensure the cells on either side have different values.
"""
class BorderConstraints(Encoder):
    @staticmethod
    def encode(solver: Solver, puzzle: Tango):
        borders = puzzle.get_borders()
        cells = puzzle.get_cells()
        for border_list in borders:
            for border in border_list:
                row1 = border.get_row()
                col1 = border.get_col()
                row2 = None
                col2 = None
                if border.is_horizontal():
                    row2 = row1 + 1
                    col2 = col1
                else:
                    row2 = row1
                    col2 = col1 + 1
                cell1 = cells[row1][col1]
                cell2 = cells[row2][col2]
                if border.is_equal():
                    solver.add(cell1.get_variable() == cell2.get_variable())
                elif border.is_different():
                    solver.add(cell1.get_variable() != cell2.get_variable())
                                    