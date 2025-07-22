from encoding.tango.tango_encoder import TangoEncoder
from encoding.queens.queens_encoder import QueensEncoder
from vision.tango_vision_bot import TangoVisionBot
from vision.queens_vision_bot import QueensVisionBot
from z3 import Solver, sat
import sys
import time

SUPPORTED_PUZZLES = ["tango", "queens"]


if __name__=="__main__":
    # Check number of args
    if len(sys.argv) != 2:
        print("Usage: python main.py tango|queens")
        sys.exit(1)
    puzzle_name = sys.argv[1].lower()

    # Check requested puzzle
    if puzzle_name not in SUPPORTED_PUZZLES:
        print(f"Puzzle '{puzzle_name}' is not supported. Supported puzzles: {'|'.join(SUPPORTED_PUZZLES)}")
        sys.exit(1)

    time_start_program = time.time()

    vision_bot = None
    if puzzle_name == "tango":
        vision_bot = TangoVisionBot()
    elif puzzle_name == "queens":
        vision_bot = QueensVisionBot()

    print("Waiting 3 seconds before taking a screenshot...")
    time.sleep(3)  # Wait for 3 seconds before taking a screenshot

    vision_bot.take_screenshot()
    vision_bot.detect_game_board()
    puzzle = vision_bot.parse_screenshot()
    print("Starting puzzle:")
    print(puzzle.get_board())
    encoder_class = None
    solver = Solver()
    if puzzle_name == "tango":
        encoder_class = TangoEncoder
    elif puzzle_name == "queens":
        encoder_class = QueensEncoder
    
    encoder_class.encode(solver, puzzle)

    print("Encoding done, solving...")
    time_start_solve = time.time()

    if solver.check() == sat:
        model = solver.model()
        time_end_solve = time.time()
        print(f"Solution found in {time_end_solve - time_start_solve:.2f} seconds.")
        cells = puzzle.get_cells()
        for var in model:
            var_split = str(var).split('_')
            row = int(var_split[1])
            col = int(var_split[2])
            cell = cells[row][col]
            cell.update_value(1 if model[var] else 0)
        print(puzzle.get_board())

    else:
        print(solver.unsat_core())
        print("No solution found.")

    time_end_program = time.time()
    print("Overall time: {:.2f} seconds.".format(time_end_program - time_start_program))
        