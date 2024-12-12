import pygame
import numpy as np

size_of_board = 600
grid_size = 5
win_condition = 5
cell_size = size_of_board // grid_size
symbol_size = (cell_size - cell_size // 4) // 2
symbol_thickness = 10
symbol_x_color = (238, 64, 53)  
symbol_o_color = (4, 146, 207)  
green_color = (123, 192, 67)   

player_x = -1
player_o = 1

pygame.init()

class TicTacToe:
    def __init__(self, role = "X"):
        self.screen = pygame.display.set_mode((size_of_board, size_of_board))
        pygame.display.set_caption("Tic Tac Toe")

        # init game
        self.board = np.zeros((grid_size, grid_size), dtype=int)
        self.player_turn = player_x if role == "X" else player_o
        self.game_over = False
        self.role = role
        self.x_wins = False
        self.o_wins = False
        self.tie = False
        self.reset_board = False
        self.x_score = 0
        self.o_score = 0
        self.tie_score = 0

    def draw_board(self):
        for i in range(1, grid_size):
            pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, size_of_board), 2)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (size_of_board, i * cell_size), 2)

    def draw_symbol(self, row, col):
        center_x = col * cell_size + cell_size // 2
        center_y = row * cell_size + cell_size // 2
        if self.board[row, col] == player_x:
            pygame.draw.line(self.screen, symbol_x_color, (center_x - symbol_size, center_y - symbol_size),
                             (center_x + symbol_size, center_y + symbol_size), symbol_thickness)
            pygame.draw.line(self.screen, symbol_x_color, (center_x - symbol_size, center_y + symbol_size),
                             (center_x + symbol_size, center_y - symbol_size), symbol_thickness)
        elif self.board[row, col] == player_o:
            pygame.draw.circle(self.screen, symbol_o_color, (center_x, center_y), symbol_size, symbol_thickness)

    def check_winner(self):
        for i in range(grid_size):
            if np.all(self.board[i, :] == player_x) or np.all(self.board[:, i] == player_x):
                self.x_wins = True
            if np.all(self.board[i, :] == player_o) or np.all(self.board[:, i] == player_o):
                self.o_wins = True

        if np.all(np.diagonal(self.board) == player_x) or np.all(np.diagonal(np.fliplr(self.board)) == player_x):
            self.x_wins = True
        if np.all(np.diagonal(self.board) == player_o) or np.all(np.diagonal(np.fliplr(self.board)) == player_o):
            self.o_wins = True

    def check_tie(self):
        if np.all(self.board != 0):
            self.tie = True

    def reset_game(self):
        self.board.fill(0)
        self.game_over = False
        self.x_wins = False
        self.o_wins = False
        self.tie = False
        self.player_turn = player_x if self.role == "X" else player_o 

    def draw_gameover(self):
        font = pygame.font.SysFont('Arial', 30)
        if self.x_wins:
            text = font.render("Player X wins!", True, symbol_x_color)
            self.x_score += 1
        elif self.o_wins:
            text = font.render("Player O wins!", True, symbol_o_color)
            self.o_score += 1
        elif self.tie:
            text = font.render("It's a tie!", True, (200, 200, 200))

        self.screen.blit(text, (size_of_board // 4, size_of_board // 4))

        score_text = f'Player X: {self.x_score}  Player O: {self.o_score}  Ties: {self.tie_score}'
        score = font.render(score_text, True, green_color)
        self.screen.blit(score, (size_of_board // 4, size_of_board // 2))

    def handle_click(self, pos):
        if self.game_over:
            self.reset_game()
            return

        col, row = pos[0] // cell_size, pos[1] // cell_size
        if self.board[row, col] == 0:
            self.board[row, col] = self.player_turn
            self.player_turn = player_o if self.player_turn == player_x else player_x

            self.check_winner()
            self.check_tie()

            if self.x_wins or self.o_wins or self.tie:
                self.game_over = True

    def run(self):
        while True:
            self.screen.fill((255, 255, 255)) 
            self.draw_board()

            for row in range(grid_size):
                for col in range(grid_size):
                    self.draw_symbol(row, col)

            if self.game_over:
                self.draw_gameover()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        self.handle_click(event.pos)

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
