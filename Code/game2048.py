# 2048.py

# importing the logic.py file
# where we have written all the
# logic functions used.
import logic

# Driver code
if __name__ == '__main__':
    
# calling start_game function
# to initialize the matrix
    mat = logic.start_game()
    for i in mat:
        print(i)

while True:
    # Taking user input
    x = input("Press the command: ")

    if x in ('W', 'w'):
        mat, flag = logic.move_up(mat)
    elif x in ('S', 's'):
        mat, flag = logic.move_down(mat)
    elif x in ('A', 'a'):
        mat, flag = logic.move_left(mat)
    elif x in ('D', 'd'):
        mat, flag = logic.move_right(mat)
    else:
        print("Invalid Key Pressed")
        continue

    # Get the game status, including invalid moves
    status = logic.get_current_state(mat, flag)

    # Handle the different statuses
    if status == 'INVALID MOVE':
        print(status)
        continue
    elif status == 'WE WON':
        print("Congratulations, you WON!")
        break
    elif status == 'GAME OVER :(':
        print("Game Over. You LOST!")
        break
    elif status == 'GAME NOT OVER':
        logic.add_new_2(mat)

    # Print the grid after each move
    for row in mat:
        print(row)