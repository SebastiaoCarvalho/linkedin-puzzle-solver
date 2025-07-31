from encoding.encoder import Encoder
from z3 import Solver, Function, IntSort
from domain.zip.zip import Zip

class NoLoopsEncoder(Encoder):
    """
    Ensure that no loops are formed in the path.
    """

    @staticmethod
    def encode(solver: Solver, puzzle: Zip) -> None:
        cells = puzzle.get_cells()
        Reach = Function("Reach", IntSort(), IntSort()) # You can reach Y from X
        Reach()