import NQueenV2
import time
import numpy as np

def getNQueensGrid(N):
    return np.array(np.zeros(shape=(N, N), dtype=int))

def runTestsNQueens(N):
    timeResults = []
    grid = getNQueensGrid(N)
    start = time.time()
    solved = NQueenV2.solveNQueensForwardChecking(grid, 0)
    end = time.time()
    timeResults.append(end - start)
    return solved

start=time.time()
solved = runTestsNQueens(12)
print(solved)
end=time.time()
print("Solved in time = ", end-start)