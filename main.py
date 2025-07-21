from parser.puzzle_parser import PuzzleParser

if __name__=="__main__":
    parser = PuzzleParser()
    puzzle_file = open("examples/tango/1.txt", "r")
    puzzle_str = puzzle_file.read()
    puzzle_file.close()
    tango = parser.parse_tango(puzzle_str)
    print(tango.get_board())