import numpy as np
from itertools import product

'''
Problem:
    Given a 4 x 4 grid, place the numbers 1 to 4 in the empty spaces, 
    satisfying the following rules:
        - There may not be a run of the same number 3 times consecutively,
          in a row, column, or diagonal.
        - There may not be the same number in the ends of a knight's move
          (i.e., in opposite corners of a 2 x 3 grid)
'''
class puzz_1234_grid_solver:
    

    '''
    Initialises the solver class.
    Inputs:
        - (numpy array) grid -> The initial state of the problem
    '''
    def __init__(self, grid):
        self.grid = grid # The solution grid


    '''
    Solve the puzzle. This should be the only method called after initiation.
    '''
    def solve(self):

        iters = 0 # Iteration counter
        self.assign_finals(self.grid) # Assign the pre-filled vaules from grid
        
        while not self.is_solved():
            self.generate_possibles() # Refine the list 'possibles' matrix
            iters += 1
        
        # If reached here, puzzle is solved
        self.iters = iters
        self.solution = self.generate_solution()
        return self.solution


    '''
    This function should only be called when each cell in 'possibles' is final.
    Generates and returns the solution grid by iterating over 'possibles'.
    '''
    def generate_solution(self):
        
        solution = np.empty([4,4],dtype=int)
        for ind in [_ for _ in product(range(4),range(4))]: # For each cell
            i,j = ind
            solution[i,j] = int(self.get_num_of_final(i,j)) # Get the value
        return solution


    '''
    Evaluates the solved state of the entire 'possibles' matrix.
    Will return true if every cell is final.
    '''
    def is_solved(self):

        return all([self.cell_is_final(ind[0],ind[1])
                   for ind in [_ for _ in product(range(4),range(4))]])


    '''
    Assigns finals to the 'possibles' matrix from the grid input. 
    This function is only called once, before the iterative solving begins.
    '''
    def assign_finals(self,grid):
        
        self.poss = np.full([4,4,4], None) # All cells start as unassigned
        # Assign cells for which there are already known solutions.
        for ind in [_ for _ in product(range(4),range(4))]: # For each cell
            i,j = ind
            if self.grid[i,j] in list(range(1,5,1)):
                self.poss[i,j] = np.array(
                    [False if n != self.grid[i,j]-1
                     else True
                     for n in range(4)])


    '''
    Iterates over the 'possibles grid'
    This will be a 4 x 4 x 4 numpy array. For each cell in self.grid,
    possibles will represent using 4 bools the possibility of that number
    being in that cell.
    '''
    def generate_possibles(self):
        
        # For nonfinal cells, assign possibles
        for ind in [_ for _ in product(range(4),range(4))]:
            i,j = ind
            
            if not self.cell_is_final(i,j): # We need to calculate the possibles

                for num in range(1,5,1): # The number to check (1,2,3,4)
                    cannot_be_num = False

                    # Check knights cells for this cell and number combo
                    for new_cell in self.get_valid_knights(i,j):
                        if (self.cell_is_final(new_cell[0],new_cell[1]) and 
                            self.get_num_of_final(new_cell[0],new_cell[1]) == num):
                            # Cannot be num
                            self.poss[i,j,num-1] = False
                            cannot_be_num = True
                            break # Don't bother checking any more
                    
                    if cannot_be_num:
                        continue # Skip the sliding window check
                    
                    # Check sliding windows for this cell and number combo
                    for window in self.get_valid_threes(i,j):
                        cells_are_num = np.full(3,False)
                        for e,offset in enumerate(window): # For each offset
                            if all(offset == np.array([0,0])): # If home cell
                                cells_are_num[e] = False
                            else:
                                new_cell = offset + np.array([i,j])
                                if (self.cell_is_final(new_cell[0],new_cell[1]) and
                                    self.get_num_of_final(new_cell[0],new_cell[1]) == num):
                                        cells_are_num[e] = True
                        # If any 2 of the 3 cells are num, cannot be num
                        if (cells_are_num == True).sum() == 2:
                            self.poss[i,j,num-1] = False
                            cannot_be_num = True
                            break # Don't bother checking any more windows

                    # If both checks have failed to rule out the cell/num combo
                    # then assign it to be possible for that cell to be num
                    if not cannot_be_num:
                        self.poss[i,j,num-1] = True


    '''
    Get the value of a cell in the possibles matrix, assuming it is final.
    '''
    def get_num_of_final(self,row,col):
        return np.where(self.poss[row,col] == True)[0][0] + 1


    '''
    Given a row and a column, returns whether or not the cell is final.
    A cell is final if it can only be one number.
    '''
    def cell_is_final(self,row, col):
        return ((self.poss[row,col] == True).sum() == 1 and
                (self.poss[row,col] == False).sum() == 3)


    '''
    Given a row and column index, returns the indexes of cells which can be
    reached using a knights move from that cell.
    Inputs row and col will be 0-indexed.
    '''
    def get_valid_knights(self,row,col):
        
        valid_offsets = []
        # Knight moves have absolute offsets of [1,2] or [2,1]
        knight_offsets = np.array([e for e in product([1,-1,2,-2],[1,-1,2,-2])])
        
        for offset in knight_offsets:
            if abs(offset[0]) == abs(offset[1]): # Filter out [1,1] and [2,2]
                continue
            # Calculate the new row and column index
            newrow = row + offset[0]
            newcol = col + offset[1]
            # If the new cell is validly placed (not out of range), then append
            if newrow in range(4) and newcol in range(4):
                valid_offsets.append([newrow,newcol])

        return valid_offsets


    '''
    Given a row and column index, returns the runs of three consecutive cells
    that include the input cell, and are valid (i.e., in range).
    Inputs row and col will be 0-indexed.
    '''
    def get_valid_threes(self,row,col):
        
        home_cell = np.array((row,col))

        row_col_offsets = list(range(-2,3,1)) # [-2, -1, 0, 1, 2]
        row_col_wd = np.array(
            [row_col_offsets[i:i+3] for i in range(len(row_col_offsets)-2)])
        
        # Generate all 12 possible sliding windows around the cell
        row_wd = [[np.array(_) for _ in zip([0,0,0],wd)] for wd in row_col_wd]
        col_wd = [[np.array(_) for _ in zip(wd,[0,0,0])] for wd in row_col_wd]
        tlbr_wd = [[np.array(_) for _ in zip(wd,wd)] for wd in row_col_wd]
        bltr_wd = [[np.array(_) for _ in zip(-1*wd,wd)] for wd in row_col_wd]

        # Return only the range-valid sliding windows
        valid_windows = []
        for windowType in [row_wd, col_wd, tlbr_wd, bltr_wd]:
            for window in windowType:
                if self.window_is_valid(home_cell,window):
                    valid_windows.append(window)
        
        return valid_windows


    '''
    Given a home cell and a window (list of three offsets), returns whether or
    not the offsets results in cells within the grid
    '''
    def window_is_valid(self,home_cell,window):
        
        offsets_valid = np.full(3,False)
        for e,offset in enumerate(window): # For each offset
            new_cell = offset + home_cell # Calculate the new cell coords
            if new_cell[0] in range(4) and new_cell[1] in range(4): # If in range
                offsets_valid[e] = True

        return all(offsets_valid) # All offsets must be valid for window to be valid
