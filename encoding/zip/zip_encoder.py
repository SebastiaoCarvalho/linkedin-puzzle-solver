from encoding.encoder import Encoder
from z3 import Solver
from domain.zip.zip import Zip
from encoding.zip.border_restrictions import BorderRestrictionsEncoder
from encoding.zip.value_restrictions import ValueRestrictionsEncoder
from encoding.zip.path_restrictions import PathRestrictionsEncoder

class ZipEncoder(Encoder):
    """
    Encode the Zip puzzle into SMT constraints.
    """

    @staticmethod
    def encode(solver: Solver, puzzle : Zip) -> None:
        BorderRestrictionsEncoder.encode(solver, puzzle)
        ValueRestrictionsEncoder.encode(solver, puzzle)
        PathRestrictionsEncoder.encode(solver, puzzle)
        