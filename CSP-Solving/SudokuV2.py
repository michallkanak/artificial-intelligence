import time, math, random


def main():
    difficulty = 1
    method = 3
    n_trials = 1

    print("Running %d difficulty(s)..." % difficulty)

    ### Easy sudoku
    easy = [[0, 3, 0, 0, 8, 0, 0, 0, 6],
            [5, 0, 0, 2, 9, 4, 7, 1, 0],
            [0, 0, 0, 3, 0, 0, 5, 0, 0],
            [0, 0, 5, 0, 1, 0, 8, 0, 4],
            [4, 2, 0, 8, 0, 5, 0, 3, 9],
            [1, 0, 8, 0, 3, 0, 6, 0, 0],
            [0, 0, 3, 0, 0, 7, 0, 0, 0],
            [0, 4, 1, 6, 5, 3, 0, 0, 2],
            [2, 0, 0, 0, 4, 0, 0, 6, 0]]

    ### Medium sudoku
    medium = [[3, 0, 8, 2, 9, 6, 0, 0, 0],
              [0, 4, 0, 0, 0, 8, 0, 0, 0],
              [5, 0, 2, 1, 0, 0, 0, 8, 7],
              [0, 1, 3, 0, 0, 0, 0, 0, 0],
              [7, 8, 0, 0, 0, 0, 0, 3, 5],
              [0, 0, 0, 0, 0, 0, 4, 1, 0],
              [1, 2, 0, 0, 0, 7, 8, 0, 3],
              [0, 0, 0, 8, 0, 0, 0, 2, 0],
              [0, 0, 0, 5, 4, 2, 1, 0, 6]]

    ### Hard sudoku
    hard = [[7, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 4, 1, 0, 2, 5, 0],
            [0, 1, 3, 0, 9, 5, 0, 0, 0],
            [8, 6, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 1, 0, 0, 0, 4, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 8, 6],
            [0, 0, 0, 8, 4, 0, 5, 3, 0],
            [0, 4, 2, 0, 3, 6, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 9]]

    ### EVIL sudoku
    evil = [[0, 6, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 4, 0, 6, 0, 0, 0, 9],
            [1, 0, 0, 0, 4, 3, 0, 6, 0],
            [0, 5, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 6, 0, 9, 3, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 7, 0],
            [0, 1, 0, 4, 8, 0, 0, 0, 5],
            [8, 0, 0, 0, 1, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 5, 0, 4, 0]]

    sudokus = [easy, medium, hard, evil]

    sudoku = sudokus[int(difficulty) - 1]

    print("sudoku to solve: ")
    print_sudoku(sudoku)

    start_time = time.time()
    method_type = int(method)

    if method_type == 1:
        print("Backtracking simple search")
        result = solve_backtrack(sudoku)
    elif method_type == 2:
        print("Backtracking with forward checking")
        result = solve_btfc(sudoku)
    else:
        print("Backtracking with forward checking and heurisitics.")
        result = solve_btfch(sudoku)

    print("Sudoku took", time.time() - start_time, "seconds.")
    return 1

# Recursive backtracking algorithm to solve sudoku
def solve_backtrack(sudoku):
    # store all the possible vals remaining for a square
    domain = range(1, 10)

    # get a list of the empty squares (remaining variables)
    empty_sqr = get_empty_squares(sudoku)

    # if there are no remaining empty squares we're done
    if len(empty_sqr) == 0:
        print("Success!")
        print_sudoku(sudoku)
        return 1

    square = get_random_square(empty_sqr)
    row = square[0]
    col = square[1]

    while len(domain) != 0:
        # get a random value out of the list of remaining possible vals
        value = domain[int(math.floor(random.random() * len(domain)))]
        domain.remove(value)
        # check the value against the constraints
        if check_row(square, value, sudoku):
            if check_col(square, value, sudoku):
                if check_block(square, value, sudoku):
                    sudoku[row][col] = value
                    if solve_backtrack(sudoku):
                        return 1
                    else:
                        sudoku[row][col] = 0
    return 0


# Backtracking with forward-checking algorithm
# Stores a list with all the variables and their potentially vals
# stop when there are no empty squares remaining
# Random select the next cell and the value
def solve_btfc(sudoku):
    # get a list of the empty squares (remaining variables)
    empty_squares = get_empty_squares(sudoku)
    # if there are no remaining empty squares - done
    if len(empty_squares) == 0:
        print("Success!")
        print_sudoku(sudoku)
        return 1

    square = get_random_square(empty_squares)
    row = square[0]
    col = square[1]

    remaining_vals = get_remaining_vals(sudoku)
    vals = list(remaining_vals[col + row * 9])

    while len(vals) != 0:
        value = vals[int(math.floor(random.random() * len(vals)))]
        vals.remove(value)
        if forward_check(remaining_vals, value, row, col):
            sudoku[row][col] = value
            if solve_btfc(sudoku):
                return 1
            else:
                sudoku[row][col] = 0

    return 0


# Solves the sudoku using forward checking and 3 heuristics:
# minimum remaining vals, degree, and least constraining value heuristics
def solve_btfch(sudoku):
    # get a list of the empty squares (remaining variables)
    empty_squares = get_empty_squares(sudoku)

    # if there are no remaining empty squares we're done
    if len(empty_squares) == 0:
        print("Success!")
        print_sudoku(sudoku)
        return 1

    # find the most constrained square (one with least remaining vals)
    remaining_vals = get_remaining_vals(sudoku)
    mrv_list = []
    [mrv_list.append(len(remaining_vals[square[0] * 9 + square[1]])) for square in empty_squares]
    # make a list of the squares with the minimum remaining vals (mrv)
    mrv_squares = []
    minimum = min(mrv_list)
    for i in range(len(mrv_list)):
        value = mrv_list[i]
        if value == minimum:
            mrv_squares.append(empty_squares[i])

    # if there are no ties, take the square with the MRV
    if len(mrv_squares) == 1:
        square = mrv_squares[0]
    else:
        # otherwise, find the most constraining variable (variable with highest degree)
        degree_list = []
        for cell in mrv_squares:
            degree = get_degree(cell, sudoku)
            degree_list.append(degree)

            max_degree = max(degree_list)
            max_degree_squares = []
            for i in range(len(degree_list)):
                value = degree_list[i]
                if value == max_degree:
                    max_degree_squares.append(mrv_squares[i])
            # just take the first square as a tie-breaker
            square = max_degree_squares[0]

    row = square[0]
    col = square[1]
    vals = list(remaining_vals[col + row * 9])

    while len(vals) != 0:
        lcv_list = get_lcv(vals, row, col, remaining_vals)
        # take the least constraining value
        value = vals[lcv_list.index(min(lcv_list))]
        vals.remove(value)
        if forward_check(remaining_vals, value, row, col):
            sudoku[row][col] = value
            if solve_btfch(sudoku):
                return 1
            else:
                sudoku[row][col] = 0

    return 0


# counts the number of times a value appears in constrained cells
def get_lcv(vals, row, col, remaining_vals):
    lcv_list = []

    for value in vals:
        count = 0
        for i in range(9):
            if i == col:
                continue
            x = remaining_vals[row * 9 + i]
            if value in x:
                count += 1

        for i in range(9):
            if i == row:
                continue
            x = remaining_vals[col + 9 * i]
            if value in x:
                count += 1

        block_row = row / 3
        block_col = col / 3
        for i in range(3):
            for j in range(3):
                if [block_row * 3 + i, block_col * 3 + j] == [row, col]:
                    continue
                x = remaining_vals[block_col * 3 + j + (block_row * 3 + i) * 9]
                if value in x:
                    count += 1

        lcv_list.append(count)

    return lcv_list


# returns the number of variables constrained by the specified square
def get_degree(square, sudoku):
    row = square[0]
    col = square[1]

    degree = 0

    for i in range(9):
        if i == col:
            continue
        if sudoku[row][i] == 0:
            degree += 1

    for i in range(9):
        if i == row:
            continue
        if sudoku[i][col] == 0:
            degree += 1

    block_row = row / 3
    block_col = col / 3
    for i in range(3):
        for j in range(3):
            if [block_row * 3 + i, block_col * 3 + j] == [row, col]:
                continue
            if sudoku[block_row * 3 + i][block_col * 3 + j] == 0:
                degree += 1

    return degree


# checks to see if the value being removed is the only one left
def forward_check(remaining_vals, value, row, col):
    for i in range(9):
        if i == col:
            continue

        x = remaining_vals[row * 9 + i]

        if len(x) == 1:
            if x[0] == value:
                return 0

    for i in range(9):
        if i == row:
            continue

        x = remaining_vals[col + 9 * i]
        if len(x) == 1:
            if x[0] == value:
                return 0

    block_row = row / 3
    block_col = col / 3
    for i in range(3):
        for j in range(3):

            if [block_row * 3 + i, block_col * 3 + j] == [row, col]:
                continue

            x = remaining_vals[block_col * 3 + j + (block_row * 3 + i) * 9]
            if len(x) == 1:
                if x[0] == value:
                    return 0
    return 1


# Returns a list of the remaining potential vals for each of the 81 squares
# The list is structured row by row with respect to the sudoku
# Only gets called once, at the beginning of the BT-FC search to initialize
def get_remaining_vals(sudoku):
    remaining_vals = []
    # initialize all remaining vals to the full domain
    [remaining_vals.append(range(1, 10)) for i in range(81)]
    for row in range(len(sudoku)):
        for col in range(len(sudoku[1])):
            if sudoku[row][col] != 0:
                # remove the value from the constrained squares
                value = sudoku[row][col]
                remaining_vals = remove_vals(row, col, value, remaining_vals)

    return remaining_vals


# Removes the specified value from constrained squares and returns the new list
def remove_vals(row, col, value, remaining_vals):
    # use a value of zero to indicate that the square is assigned
    remaining_vals[col + row * 9] = [0]

    # Remove the specified value from each row, column, and block if it's there
    for x in remaining_vals[row * 9:row * 9 + 9]:
        try:
            x.remove(value)
        except ValueError:
            pass

    for i in range(9):
        try:
            remaining_vals[col + 9 * i].remove(value)
        except ValueError:
            pass

    block_row = row / 3
    block_col = col / 3
    for i in range(3):
        for j in range(3):
            try:
                remaining_vals[block_col * 3 + j + (block_row * 3 + i) * 9].remove(value)
            except ValueError:
                pass

    return remaining_vals


# return a randomly selected square from the list of empties
def get_random_square(empty_squares):
    # randomly pick one of the empty squares to expand and return it
    return empty_squares[int(math.floor(random.random() * len(empty_squares)))]


# return the list of empty squares indices for the sudoku
def get_empty_squares(sudoku):
    empty_squares = []
    # scan the whole sudoku for empty cells
    for row in range(len(sudoku)):
        for col in range(len(sudoku[1])):
            if sudoku[row][col] == 0:
                empty_squares.append([row, col])
    return empty_squares


# checks the 9x9 block to which the square belongs
def check_block(square, value, sudoku):
    row = square[0]
    col = square[1]
    block_row = row / 3
    block_col = col / 3

    for i in range(3):
        for j in range(3):
            if [i, j] == square:
                continue
            if sudoku[block_row * 3 + i][block_col * 3 + j] == value:
                return 0
    return 1


# checks the row of the specified square for the same val
def check_row(square, value, sudoku):
    row = square[0]
    col = square[1]
    for i in range(len(sudoku)):
        if i == square[0]:
            continue
        if sudoku[row][i] == value:
            return 0

    return 1


# checks the column of the specified square for the same val
def check_col(square, value, sudoku):
    row = square[0]
    col = square[1]
    for i in range(len(sudoku[1])):
        if i == square[1]:
            continue
        if sudoku[i][col] == value:
            return 0

    return 1


def print_sudoku(sudoku):
    for row in sudoku:
        print(row)


if __name__ == "__main__":
    main()
