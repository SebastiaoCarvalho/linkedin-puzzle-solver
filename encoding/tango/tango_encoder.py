from z3 import Solver
from domain.tango.tango import Tango
from encoding.encoder import Encoder
from encoding.tango.no_3_consecutives import No3Consecutives
from encoding.tango.equal_number import EqualNumber
from encoding.tango.static_cells import StaticCells
from encoding.tango.border_constraints import BorderConstraints

"""
Encoder for Tango puzzles.
"""

class TangoEncoder(Encoder):
    @staticmethod
    def encode(solver: Solver, puzzle: Tango):
        No3Consecutives.encode(solver, puzzle)
        EqualNumber.encode(solver, puzzle)
        StaticCells.encode(solver, puzzle)
        BorderConstraints.encode(solver, puzzle)