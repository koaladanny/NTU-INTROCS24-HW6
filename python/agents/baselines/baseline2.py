import random
from agents.agent import AgentBase
from copy import deepcopy

class Agent(AgentBase):
    def __init__(self, name, symbol, game_config):
        super().__init__(name, symbol, game_config)
        self.num_cols = game_config['num_cols']
        self.num_rows = game_config['num_rows']
        self.win_n = game_config['win_n']

    def find_available_moves(self, board):
        return [col for col in range(self.num_cols) if any(board[row][col] == 0 for row in range(self.num_rows))]
    
    def is_winner(self, board):
        # check horizontal
        for row in range(self.num_rows):
            for col in range(self.num_cols - self.win_n + 1):
                if all(board[row][col + i] == self._symbol for i in range(self.win_n)):
                    return True
        
        # check vertical
        for row in range(self.num_rows - self.win_n + 1):
            for col in range(self.num_cols):
                if all(board[row + i][col] == self._symbol for i in range(self.win_n)):
                    return True
        
        # check diagonal
        for row in range(self.num_rows - self.win_n + 1):
            for col in range(self.num_cols - self.win_n + 1):
                if all(board[row + i][col + i] == self._symbol for i in range(self.win_n)):
                    return True
                
                if all(board[row + i][col + self.win_n - i - 1] == self._symbol for i in range(self.win_n)):
                    return True
        
        return False
    
    def update_board(self, board, col):
        new_board = deepcopy(board)
        for row in range(self.num_rows - 1, -1, -1):
            if new_board[row][col] == 0:
                new_board[row][col] = self._symbol
                return new_board
            
        return new_board


    def get_move(self, board):
        moves = self.find_available_moves(board)
        # if any moves can lead to a win, return that move
        for col in moves:
            updated_board = self.update_board(board, col)
            if self.is_winner(updated_board):
                return col
            
        # otherwise, return a random move
        return random.choice(self.find_available_moves(board))