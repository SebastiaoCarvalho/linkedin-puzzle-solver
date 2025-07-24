from encoding.encoder import Encoder
from z3 import Solver, Sum
from domain.tango.tango import Tango

class EqualNumber(Encoder):
    """
    Need an equal number of Suns and Moons in each row and column.
    """

    @staticmethod
    def encode(solver: Solver, puzzle: Tango):
        cells = puzzle.get_cells()
        rows = len(cells)
        cols = len(cells[0])

        # Ensure equal number of Suns and Moons in each row
        for i in range(rows):
            solver.add(
                Sum([cells[i][j].get_variable() for j in range(cols)]) == rows // 2
            )

        # Ensure equal number of Suns and Moons in each column
        for j in range(cols):
            solver.add(
                Sum([cells[i][j].get_variable() for i in range(rows)]) == cols // 2
            )