from z3 import Solver
from domain.puzzle import Puzzle

class Encoder:
    """
    Base class for SMT encoder.
    """

    @staticmethod
    def encode(solver: Solver, puzzle : Puzzle) -> None:
        pass