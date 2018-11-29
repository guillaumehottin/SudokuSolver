def get_position_from_line_and_column(line, column, size=9):
    return line*size + column


def import_grid_from_file(filename):
    with open(filename) as file:
        text = file.read().replace('\n', '')
        grid = [int(text[get_position_from_line_and_column(i, j)]) for i in range(9) for j in range(9)]

    return grid


def pretty_print_grid(grid):
    grid_string = ""
    for i in range(9):
        if i == 3 or i == 6:
            grid_string += "---+---+---\n"
        line_string = ""
        for j in range(9):
            element_string = ""
            if j == 3 or j == 6:
                element_string += '|'
            element_string += str(grid[get_position_from_line_and_column(i, j)]) \
                if grid[get_position_from_line_and_column(i, j)] != 0 else ' '
            line_string += element_string
        grid_string += line_string + '\n'

    print(grid_string)


def get_non_used_numbers(numbers):
    non_used_numbers = []

    for i in range(9):
        if (i+1) not in numbers:
            non_used_numbers.append(i+1)

    return non_used_numbers


def possible_from_vertical_line(grid, column):
    vertical_line = [grid[get_position_from_line_and_column(line, column)] for line in range(9)]
    return get_non_used_numbers(vertical_line)


def possible_from_horizontal_line(grid, line):
    horizontal_line = [grid[get_position_from_line_and_column(line, column)] for column in range(9)]
    return get_non_used_numbers(horizontal_line)


def possible_from_sub_grid(grid, line, column):
    start_line = int(line/3) * 3
    start_column = int(column/3) * 3
    sub_grid = [grid[get_position_from_line_and_column(i, j)] for i in range(start_line, start_line + 3)
                for j in range(start_column, start_column + 3)]
    return get_non_used_numbers(sub_grid)


def possible_from_position(grid, line, column):
    possible_horizontal = possible_from_horizontal_line(grid, line)
    possible_vertical = possible_from_vertical_line(grid, column)
    possible_sub_grid = possible_from_sub_grid(grid, line, column)
    possible_numbers = []

    for i in range(9):
        if (i+1) in possible_horizontal and (i+1) in possible_vertical and (i+1) in possible_sub_grid:
            possible_numbers.append(i+1)

    return possible_numbers


def solve_grid(grid):
    new_grid = grid.copy()
    at_least_one_found = True

    while at_least_one_found:
        at_least_one_found = False
        for i in range(9):
            for j in range(9):
                if new_grid[get_position_from_line_and_column(i, j)] == 0:
                    possible_numbers = possible_from_position(new_grid, i, j)
                    if len(possible_numbers) == 1:
                        new_grid[get_position_from_line_and_column(i, j)] = possible_numbers[0]
                        at_least_one_found = True

    grid_done = 0 not in new_grid
    if not grid_done:
        hypothesis_index = new_grid.index(0)
        possible_numbers = possible_from_position(new_grid, int(hypothesis_index/9), hypothesis_index % 9)
        new_grids = []

        for possible_number in possible_numbers:
            hypothetical_grid = new_grid.copy()
            hypothetical_grid[hypothesis_index] = possible_number
            new_grids.append(hypothetical_grid)

        for hypothetical_grid in new_grids:
            solved_hypothetical_grid, solved = solve_grid(hypothetical_grid)
            if solved:
                return solved_hypothetical_grid, True

    return new_grid, grid_done


my_grid = import_grid_from_file("grid.txt")
pretty_print_grid(my_grid)
solved_grid, is_solved = solve_grid(my_grid)
print(is_solved)
pretty_print_grid(solved_grid)
