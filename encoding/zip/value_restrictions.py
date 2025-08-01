from encoding.encoder import Encoder
from z3 import Solver
from domain.zip.zip import Zip

class ValueRestrictionsEncoder(Encoder):
    """
    Values need to be between 0 and 3 (L, R, U, D).
    """

    @staticmethod
    def encode(solver: Solver, puzzle: Zip):
        cells = puzzle.get_cells()
        for row in cells:
            for cell in row:
                value_var = cell.get_variable()
                if puzzle.exists_number(cell.get_row(), cell.get_col()) and puzzle.get_number(cell.get_row(), cell.get_col()).get_value() == puzzle.get_last_number().get_value():
                    # Last number should not have any operation
                    solver.add(value_var == 4)  # Assuming 4 represents 'X' (no operation)
                else:
                    solver.add(value_var >= 0, value_var <= 3)
