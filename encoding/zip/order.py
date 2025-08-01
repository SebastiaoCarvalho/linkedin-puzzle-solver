from encoding.encoder import Encoder
from z3 import Solver
from domain.zip.zip import Zip

class OrderEncoder(Encoder):
    """
    Ensure that the path follows the order of numbers in the Zip puzzle.
    The path must start at 1 and end at the last number, with each number
    being visited in increasing order.
    """

    @staticmethod
    def encode(solver: Solver, puzzle: Zip):
        cells = puzzle.get_cells()
        numbers = puzzle.get_numbers_sorted()
        Reach = puzzle.get_reach()
        for i in range(1, len(numbers) - 1):
            current_number = numbers[i]
            next_number = numbers[i + 1]
            current_cell = cells[current_number.get_row()][current_number.get_col()]
            next_cell = cells[next_number.get_row()][next_number.get_col()]

            # Ensure that the path from current to next number is valid
            solver.add(Reach(current_cell.get_col(), current_cell.get_row(),
                        next_cell.get_col(), next_cell.get_row()))
        