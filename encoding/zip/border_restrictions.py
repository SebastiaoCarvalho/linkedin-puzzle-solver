from encoding.encoder import Encoder
from z3 import Solver
from domain.zip.zip import Zip

class BorderRestrictionsEncoder(Encoder):
    """
    Cells in the top row cannot go Up, cells in the bottom row cannot go Down,
    cells in the leftmost column cannot go Left, and cells in the rightmost column
    cannot go Right.
    """

    @staticmethod
    def encode(solver: Solver, puzzle: Zip):
        cells = puzzle.get_cells()

        for cell in cells[0]:
            # Top row cannot go Up
            solver.add(cell.get_variable() != 2)

        for cell in cells[-1]:
            # Bottom row cannot go Down
            solver.add(cell.get_variable() != 3)

        for cell in [row[0] for row in cells]:
            # Leftmost column cannot go Left
            solver.add(cell.get_variable() != 0)

        for cell in [row[-1] for row in cells]:
            # Rightmost column cannot go Right
            solver.add(cell.get_variable() != 1)
