from encoding.encoder import Encoder
from z3 import Solver, Not
from domain.tango.tango import Tango

class StaticCells(Encoder):
    """
    Cells that are static and do not change their state.
    """

    @staticmethod
    def encode(solver: Solver, puzzle: Tango):
        for row in puzzle.get_cells():
            for cell in row:
                if cell.is_static():
                    solver.add(cell.get_variable()) if cell.get_value_bool() else solver.add(Not(cell.get_variable()))