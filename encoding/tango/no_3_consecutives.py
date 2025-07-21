from encoding.encoder import Encoder
from z3 import Solver, Not, And
from domain.tango.tango import Tango

"""
Cannot have 3 suns or moons consecutively in a row or column.
"""
class No3Consecutives(Encoder):
    @staticmethod
    def encode(solver : Solver, puzzle : Tango):
        cells = puzzle.get_cells()
        rows = len(cells)
        cols = len(cells[0])
        
        # Forbid 3 consecutive suns or moons in rows
        for i in range(rows):
            for j in range(cols - 2):
                solver.add(
                    Not(
                        And(
                            cells[i][j].get_variable() == 0,
                            cells[i][j + 1].get_variable() == 0,
                            cells[i][j + 2].get_variable() == 0
                        )
                    )
                )
                solver.add(
                    Not(
                        And(
                            cells[i][j].get_variable() == 1,
                            cells[i][j + 1].get_variable() == 1,
                            cells[i][j + 2].get_variable() == 1
                        )
                    )
                )
        # Forbid 3 consecutive suns or moons in columns
        for j in range(cols):
            for i in range(rows - 2):
                solver.add(
                    Not(
                        And(
                            cells[i][j].get_variable() == 0,
                            cells[i + 1][j].get_variable() == 0,
                            cells[i + 2][j].get_variable() == 0
                        )
                    )
                )
                solver.add(
                    Not(
                        And(
                            cells[i][j].get_variable() == 1,
                            cells[i + 1][j].get_variable() == 1,
                            cells[i + 2][j].get_variable() == 1
                        )
                    )
                )
        
                