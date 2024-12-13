# logic.py to be 
# imported in the 2048.py file

# importing random package
# for methods to generate random
# numbers.
import random

# function to initialize game / mat
# at the start
def start_game():
    # Initialize the 4x4 grid with zeros
    mat = [[0] * 4 for _ in range(4)]

    # Add the first two tiles (2's) to the grid
    add_new_2(mat)
    add_new_2(mat)

    # Return the initialized grid
    return mat

# Function to add a new '2' in a random empty cell in the grid
def add_new_2(mat):
    # Find all empty cells (cells with 0)
    empty_cells = [(i, j) for i in range(4) for j in range(4) if mat[i][j] == 0]

    # If there are no empty cells, return (board is full)
    if not empty_cells:
        return

    # Choose a random empty cell from the list
    r, c = random.choice(empty_cells)

    # Place a '2' in the randomly chosen empty cell
    mat[r][c] = 2

# function to get the current
# state of game
def get_current_state(mat, flag):
    # Check if the game is won
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 2048:
                return 'WE WON'

    # Check if no valid moves exist (either no empty cells and no possible merges)
    for i in range(4):
        for j in range(4):
            current_value = mat[i][j]
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = i + dr, j + dc
                if 0 <= nr < 4 and 0 <= nc < 4 and (mat[nr][nc] == current_value or mat[nr][nc] == 0):
                    return 'GAME NOT OVER'  # A valid move exists, game is not over

    # If no empty cells and no valid moves, game is over
    if all(mat[i][j] != 0 for i in range(4) for j in range(4)):
        return 'GAME OVER :('

    # If the flag is False and no valid moves left, check for invalid move
    if not flag:
        return 'INVALID MOVE'

    # If none of the above, the game is still ongoing and no invalid move was made
    return 'GAME NOT OVER'
    

# all the functions defined below
# are for left swap initially.

# function to compress the mat
# after every step before and
# after merging cells.
def compress(mat):

    # bool variable to determine
    # any change happened or not
    changed = False

    # empty mat 
    new_mat = []

    # with all cells empty
    for i in range(4):
        new_mat.append([0] * 4)
        
    # here we will shift entries
    # of each cell to it's extreme
    # left i by i
    # loop to traverse is
    for i in range(4):
        pos = 0

        # loop to traverse each jumn
        # in respective i
        for j in range(4):
            if(mat[i][j] != 0):
                
                # if cell is non empty then
                # we will shift it's number to
                # previous empty cell in that i
                # denoted by pos variable
                new_mat[i][pos] = mat[i][j]
                
                if(j != pos):
                    changed = True
                pos += 1

    # returning new compressed matrix
    # and the flag variable.
    return new_mat, changed

# function to merge the cells
# in matrix after compressing
def merge(mat):
    
    changed = False
    
    for i in range(4):
        for j in range(3):

            # if current cell has same value as
            # next cell in the i and they
            # are non empty then
            if(mat[i][j] == mat[i][j + 1] and mat[i][j] != 0):

                # double current cell value and
                # empty the next cell
                mat[i][j] = mat[i][j] * 2
                mat[i][j + 1] = 0

                # make bool variable True indicating
                # the new mat after merging is
                # different.
                changed = True

    return mat, changed

# function to reverse the matrix
# means reversing the content of
# each i (reversing the sequence)
def reverse(mat):
    new_mat =[]
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][3 - j])
    return new_mat

# function to get the transpose
# of matrix means interchanging
# is and jumn
def transpose(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[j][i])
    return new_mat

# function to update the matrix
# if we move / swipe left
def move_left(mat):
    # First compress the mat
    new_mat, changed1 = compress(mat)

    # Then merge the cells
    new_mat, changed2 = merge(new_mat)

    # Second compression to shift tiles after merging
    new_mat, changed3 = compress(new_mat)

    # Determine if any changes occurred (only if a valid shift or merge happened)
    changed = changed1 or changed2 or changed3

    # Check if new blocks were added, but no valid moves occurred
    if not changed and any(mat[i][j] == 0 for i in range(4) for j in range(4)):
        # If there are new blocks, but no moves were made, set changed to False
        return mat, False  # No move or merge happened
    
    # Return new mat and the correct flag
    return new_mat, changed

# function to update the matrix
# if we move / swipe right
def move_right(mat):
    new_mat = reverse(mat)
    new_mat, changed = move_left(new_mat)
    new_mat = reverse(new_mat)
    return new_mat, changed

# function to update the matrix
# if we move / swipe up
def move_up(mat):
    new_mat = transpose(mat)
    new_mat, changed = move_left(new_mat)
    new_mat = transpose(new_mat)
    return new_mat, changed

# function to update the matrix
# if we move / swipe down
def move_down(mat):
    new_mat = transpose(mat)
    new_mat, changed = move_left(new_mat)
    new_mat = transpose(new_mat)
    return new_mat, changed

# this file only contains all the logic
# functions to be called in main function
# present in the other file