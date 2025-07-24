from z3 import Solver, Sum
from domain.queens.queens import Queens
from encoding.encoder import Encoder

class OnePerRowColumn(Encoder):
    """
    One queen per row and one queen per column.
    """

    @staticmethod
    def encode(solver : Solver, puzzle : Queens):
        cells = puzzle.get_cells()
        n = len(cells)

        # Ensure that each row has exactly one queen
        for i in range(n):
            solver.add(Sum([cells[i][j].get_variable() for j in range(n)]) == 1)

        # Ensure that each column has exactly one queen
        for j in range(n):
            solver.add(Sum([cells[i][j].get_variable() for i in range(n)]) == 1)