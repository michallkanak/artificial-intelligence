# lib file
def solveNQueensBacktracking(grid, hetman):
    if len(grid) == hetman:
        print(grid)
        return True
    rowsPropos = getRowsProposition(grid, hetman)
    for row in rowsPropos:
        if isCorrect(grid, row, hetman):
            grid[row, hetman] = 1
            if solveNQueensBacktracking(grid, hetman + 1):
                return True
            grid[row, hetman] = 0
    return False


def solveNQueensForwardChecking(grid, hetman):
    if len(grid) == hetman:
        print(grid)
        return True
    rowsPropos = getRowsProposition(grid, hetman)
    for row in rowsPropos:
        grid[row, hetman] = 1
        domainWipeOut = False
        for variable in getUnassignedFromConstraint(grid, hetman):
            if fc(grid, variable.row, variable.col):
                domainWipeOut = True
                break
        if not domainWipeOut:
            if solveNQueensForwardChecking(grid, hetman + 1):
                return True
        grid[row, hetman] = 0


# utils methods
def getUnassignedFromConstraint(grid, hetman):
    result = []
    for row in range(len(grid)):
        for col in range(hetman + 1, len(grid)):
            if grid[row, col] == 0 and isCorrect(grid, row, col):
                result.append(Unassigned(row, col))
    return result


def fc(grid, row, hetman):
    actualDomain = getRowsProposition(grid, hetman)
    tempDomain = list(actualDomain)
    for propositionRow in actualDomain:
        if not isCorrect(grid, propositionRow, hetman):
            tempDomain.remove(propositionRow)
    return len(tempDomain) == 0


def isCorrect(grid, row, col):
    return isRowCorrect(grid, row) and isColumnCorrect(grid, col) and isDiagonalCorrect(grid, row, col)


def isRowCorrect(grid, row):
    for col in range(len(grid)):
        if grid[row, col] == 1:
            return False
    return True


def isColumnCorrect(grid, col):
    for row in range(len(grid)):
        if grid[row, col] == 1:
            return False
    return True


def checkUpperDiagonal(grid, row, col):
    iterRow = row
    iterCol = col
    while iterCol >= 0 and iterRow >= 0:
        if grid[iterRow, iterCol] == 1:
            return False
        iterCol -= 1
        iterRow -= 1
    return True


def checkLowerDiagonal(grid, row, col):
    iterRow = row
    iterCol = col
    while iterCol >= 0 and iterRow < len(grid):
        if grid[iterRow, iterCol] == 1:
            return False
        iterRow += 1
        iterCol -= 1
    return True


def isDiagonalCorrect(grid, row, col):
    return checkUpperDiagonal(grid, row, col) and checkLowerDiagonal(grid, row, col)


def getRowsProposition(grid, hetman):
    rows = []
    for row in range(len(grid)):
        if isCorrect(grid, row, hetman):
            rows.append(row)
    return rows


class Unassigned:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash(self.row) ^ hash(self.col)
