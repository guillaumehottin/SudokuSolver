from sudoku_solver import solve_grid, import_grid_from_file, pretty_print_grid
import argparse

parser = argparse.ArgumentParser(description='Solve a sudoku grid.')
parser.add_argument('filepath', help='Path to the grid file')
parser.add_argument('--print_unsolved', action='store_true', help='Print the unsolved grid')
args = parser.parse_args()

grid = import_grid_from_file(args.filepath)

if args.print_unsolved:
    pretty_print_grid(grid)

solved_grid, solved = solve_grid(grid)

if solved:
    pretty_print_grid(solved_grid)
else:
    print("Could not solve the provided grid")