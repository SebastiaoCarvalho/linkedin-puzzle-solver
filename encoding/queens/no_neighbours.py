from z3 import Solver, Implies, And, Not
from domain.queens.queens import Queens
from encoding.encoder import Encoder

class NoNeighbours(Encoder):

    @staticmethod
    def encode(solver : Solver, puzzle : Queens):
        cells = puzzle.get_cells()
        n = len(cells)

        # Ensure that no two queens are in adjacent cells
        for i in range(n):
            for j in range(n):
                neighbours = []
                has_up = i > 0
                has_down = i < n - 1
                has_left = j > 0
                has_right = j < n - 1
                if has_up:
                    neighbours.append(cells[i - 1][j].get_variable())
                if has_down:
                    neighbours.append(cells[i + 1][j].get_variable())
                if has_left:
                    neighbours.append(cells[i][j - 1].get_variable())
                if has_right:
                    neighbours.append(cells[i][j + 1].get_variable())
                if has_up and has_left:
                    neighbours.append(cells[i - 1][j - 1].get_variable())
                if has_up and has_right:
                    neighbours.append(cells[i - 1][j + 1].get_variable())
                if has_right and has_down:
                    neighbours.append(cells[i + 1][j + 1].get_variable())
                if has_left and has_down:
                    neighbours.append(cells[i + 1][j - 1].get_variable())
                if neighbours:
                    solver.add(
                        Implies(
                            cells[i][j].get_variable(),
                            And(
                                [
                                   Not(neighbour) for neighbour in neighbours
                                ]
                            )
                        )
                    )
                
                    
