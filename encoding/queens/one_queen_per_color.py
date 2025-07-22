from z3 import Solver, Sum
from domain.queens.queens import Queens
from encoding.encoder import Encoder

class OneQueenPerColor(Encoder):

    @staticmethod
    def encode(solver: Solver, puzzle: Queens):
        cells = puzzle.get_cells()
        n = len(cells)

        colors = set()
        for i in range(n):
            for j in range(n):
                if cells[i][j].get_color() is not None:
                    colors.add(cells[i][j].get_color())
        colors = list(colors)
        
        for color in colors:
            cells_with_color = [
                cells[i][j].get_variable() for i in range(n) for j in range(n)
                if cells[i][j].get_color() == color
            ]
            # Ensure that there is exactly one queen for each color
            solver.add(Sum(cells_with_color) == 1)