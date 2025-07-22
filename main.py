from parser.puzzle_parser import PuzzleParser
from encoding.tango.tango_encoder import TangoEncoder
from z3 import Solver, sat

if __name__=="__main__":
    parser = PuzzleParser()
    puzzle_file = open("examples/tango/1.txt", "r")
    puzzle_str = puzzle_file.read()
    puzzle_file.close()
    tango = parser.parse_tango(puzzle_str)
    print("Starting Tango puzzle:")
    print(tango.get_board())
    solver = Solver()
    TangoEncoder.encode(solver, tango)

    if solver.check() == sat:
        model = solver.model()
        print("Solution found:")
        cells = tango.get_cells()
        for var in model:
            var_split = str(var).split('_')
            row = int(var_split[1])
            col = int(var_split[2])
            cell = cells[row][col]
            cell.update_value(1 if model[var] else 0)
        print(tango.get_board())
            
    else:
        print(solver.unsat_core())
        print("No solution found.")    