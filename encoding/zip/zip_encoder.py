from encoding.encoder import Encoder
from z3 import Solver
from domain.zip.zip import Zip

class ZipEncoder(Encoder):

    @staticmethod
    def encode(solver: Solver, puzzle : Zip) -> None:
        """
        Encode the Zip puzzle into SMT constraints.
        """

        pass