from encoding.encoder import Encoder
from z3 import Solver, Function, IntSort, BoolSort, ForAll, Ints, Implies, Not, And
from domain.zip.zip import Zip

class NoLoopsEncoder(Encoder):
    """
    Ensure that no loops are formed in the path.
    """

    @staticmethod
    def encode(solver: Solver, puzzle: Zip) -> None:
        cells = puzzle.get_cells()

        Reach = puzzle.get_reach()
        x1, x2, y1, y2, z1, z2  = Ints("x1 x2 y1 y2 z1 z2")
        # If you can reach Y from X, then you cannot reach X from Y
        solver.add(ForAll([x1, x2, y1, y2], Implies(Reach(x1, x2, y1, y2), Not(Reach(y1, y2, x1, x2)))))
        # If you can reach Y from X, and Z from Y, then you can reach Z from X
        solver.add(ForAll([x1, x2, y1, y2, z1, z2], Implies(And(Reach(x1, x2, y1, y2), Reach(y1, y2, z1, z2)), Reach(x1, x2, z1, z2))))
        for row in cells:
            for cell in row:
                var = cell.get_variable()
                y = cell.get_row()
                x = cell.get_col()
                if y > 0:
                    solver.add(Implies(var == 3, Reach(x, y, x, y - 1)))
                if y < len(cells) - 1:
                    solver.add(Implies(var == 2, Reach(x, y, x, y + 1)))
                if x > 0:
                    solver.add(Implies(var == 0, Reach(x, y, x - 1, y)))
                if x < len(cells[0]) - 1:
                    solver.add(Implies(var == 1, Reach(x, y, x + 1, y)))
        # Start can reach all cells and all cells reach end
        start = puzzle.get_first_number()
        end = puzzle.get_last_number()
        for row in cells:
            for cell in row:
                if cell.get_row() != start.get_row() or cell.get_col() != start.get_col():
                    solver.add(Reach(start.get_col(), start.get_row(), cell.get_col(), cell.get_row()))
                if cell.get_row() != end.get_row() or cell.get_col() != end.get_col():
                    solver.add(Reach(cell.get_col(), cell.get_row(), end.get_col(), end.get_row()))