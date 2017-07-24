# Example usage of the puzz_1234_grid_solver class

from puzz_1234 import *
 

puzzle = puzz_1234_grid_solver(np.array([[1,1,0,0],
                                         [0,1,0,2],
                                         [2,0,0,2],
                                         [0,0,4,3]]))
print(puzzle.grid)
solution = puzzle.solve()
print("Solution found in", puzzle.iters, "iterations")
print(solution)
