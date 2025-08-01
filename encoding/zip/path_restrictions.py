from encoding.encoder import Encoder
from z3 import Solver, Or, Implies, Not
from domain.zip.zip import Zip

class PathRestrictionsEncoder(Encoder):
    """
    Start in cell with number 1.
    All cells except 1st and last number cells must have at least one path to a neighbor cell.
    """
    @staticmethod
    def encode(solver: Solver, puzzle: Zip):
        cells = puzzle.get_cells()
        for row in cells:
            for cell in row:
                # Case where it's number 1 cell
                if puzzle.exists_number(cell.get_row(), cell.get_col()) and puzzle.get_number(cell.get_row(), cell.get_col()).get_value() == 1:
                    # Block paths to it
                    if cell.get_row() > 0:
                        solver.add(cells[cell.get_row() - 1][cell.get_col()].get_variable() != 3)
                    if cell.get_row() < len(cells) - 1:
                        solver.add(cells[cell.get_row() + 1][cell.get_col()].get_variable() != 2)
                    if cell.get_col() > 0:
                        solver.add(cells[cell.get_row()][cell.get_col() - 1].get_variable() != 1)
                    if cell.get_col() < len(cells[0]) - 1:
                        solver.add(cells[cell.get_row()][cell.get_col() + 1].get_variable() != 0)
                # Case where it's last number cell
                elif puzzle.exists_number(cell.get_row(), cell.get_col()) and puzzle.get_number(cell.get_row(), cell.get_col()).get_value() == puzzle.get_last_number().get_value():
                    pass # Value encoding already handles this
                # Case where it's not first or last number cell
                else:
                    possibilities = []
                    if cell.get_row() > 0:
                        possibilities.append(cells[cell.get_row() - 1][cell.get_col()].get_variable() == 3)
                    if cell.get_row() < len(cells) - 1:
                        possibilities.append(cells[cell.get_row() + 1][cell.get_col()].get_variable() == 2)
                    if cell.get_col() > 0:
                        possibilities.append(cells[cell.get_row()][cell.get_col() - 1].get_variable() == 1)
                    if cell.get_col() < len(cells[0]) - 1:
                        possibilities.append(cells[cell.get_row()][cell.get_col() + 1].get_variable() == 0)
                    or_clause = Or(*possibilities)
                    solver.add(or_clause)
                    for i in range(len(possibilities)):
                        other_possibilities = possibilities[:i] + possibilities[i+1:]
                        solver.add(Implies(possibilities[i], Not(Or(*other_possibilities))))
                    
                    

                    
                