from math import sqrt


def get_position_from_line_and_column(line, column, size):
    return line*size + column


def import_grid_from_file(filename):
    with open(filename) as file:
        text = file.read().replace('\n', '')
        tab = text.split(',')
        grid = [int(number) for number in tab]

    return grid


def pad_number(number, grid_size):
    return (len(str(grid_size))*' ' + str(number))[-len(str(grid_size)):]


def pretty_print_grid(grid):
    grid_string = ""
    grid_size = int(sqrt(len(grid)))
    for i in range(grid_size):
        if i > 0 and i % sqrt(grid_size) == 0:
            grid_string += (int(sqrt(grid_size)) - 1)*(int(sqrt(grid_size))*(len(str(grid_size)) + 1)*'-' + '+') + \
                           int(sqrt(grid_size)) * (len(str(grid_size)) + 1) * '-' + '\n'
        line_string = ""
        for j in range(grid_size):
            element_string = ""
            if j > 0 and j % sqrt(grid_size) == 0:
                element_string += '|'
            element_string += pad_number(grid[get_position_from_line_and_column(i, j, grid_size)], grid_size) + ' ' \
                if grid[get_position_from_line_and_column(i, j, grid_size)] != 0 else (len(str(grid_size)) + 1)*' '
            line_string += element_string
        grid_string += line_string + '\n'

    print(grid_string)


def get_non_used_numbers(numbers, grid_size):
    non_used_numbers = []

    for i in range(grid_size):
        if (i+1) not in numbers:
            non_used_numbers.append(i+1)

    return non_used_numbers


def possible_from_vertical_line(grid, column):
    grid_size = int(sqrt(len(grid)))
    vertical_line = [grid[get_position_from_line_and_column(line, column, grid_size)] for line in range(grid_size)]
    return get_non_used_numbers(vertical_line, grid_size)


def possible_from_horizontal_line(grid, line):
    grid_size = int(sqrt(len(grid)))
    horizontal_line = [grid[get_position_from_line_and_column(line, column, grid_size)] for column in range(grid_size)]
    return get_non_used_numbers(horizontal_line, grid_size)


def possible_from_sub_grid(grid, line, column):
    grid_size = int(sqrt(len(grid)))
    start_line = int(line/int(sqrt(grid_size))) * int(sqrt(grid_size))
    start_column = int(column/int(sqrt(grid_size))) * int(sqrt(grid_size))
    sub_grid = [grid[get_position_from_line_and_column(i, j, grid_size)] for i in
                range(start_line, start_line + int(sqrt(grid_size)))
                for j in range(start_column, start_column + int(sqrt(grid_size)))]
    return get_non_used_numbers(sub_grid, grid_size)


def possible_from_position(grid, line, column):
    possible_horizontal = possible_from_horizontal_line(grid, line)
    possible_vertical = possible_from_vertical_line(grid, column)
    possible_sub_grid = possible_from_sub_grid(grid, line, column)
    possible_numbers = []
    grid_size = int(sqrt(len(grid)))

    for i in range(grid_size):
        if (i+1) in possible_horizontal and (i+1) in possible_vertical and (i+1) in possible_sub_grid:
            possible_numbers.append(i+1)

    return possible_numbers


def solve_grid(grid):
    new_grid = grid.copy()
    at_least_one_found = True
    grid_size = int(sqrt(len(grid)))

    while at_least_one_found:
        at_least_one_found = False
        for i in range(grid_size):
            for j in range(grid_size):
                if new_grid[get_position_from_line_and_column(i, j, grid_size)] == 0:
                    possible_numbers = possible_from_position(new_grid, i, j)
                    if len(possible_numbers) == 1:
                        new_grid[get_position_from_line_and_column(i, j, grid_size)] = possible_numbers[0]
                        at_least_one_found = True

    grid_done = 0 not in new_grid
    if not grid_done:
        hypothesis_index = new_grid.index(0)
        possible_numbers = possible_from_position(new_grid, int(hypothesis_index/grid_size),
                                                  hypothesis_index % grid_size)
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
