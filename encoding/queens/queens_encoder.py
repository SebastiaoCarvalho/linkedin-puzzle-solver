from z3 import Solver
from domain.queens.queens import Queens
from encoding.encoder import Encoder
from encoding.queens.no_neighbours import NoNeighbours
from encoding.queens.one_per_row_column import OnePerRowColumn
from encoding.queens.one_queen_per_color import OneQueenPerColor


class QueensEncoder(Encoder):
    """
    Encodes the constraints for the Queens puzzle.
    """

    @staticmethod
    def encode(solver : Solver, puzzle : Queens):
        # Encode the constraints for the Queens puzzle
        NoNeighbours.encode(solver, puzzle)
        OnePerRowColumn.encode(solver, puzzle)
        OneQueenPerColor.encode(solver, puzzle)
