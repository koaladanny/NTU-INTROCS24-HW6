import random
from agents.agent import AgentBase

class Agent(AgentBase):
    def __init__(self, name, symbol, game_config):
        super().__init__(name, symbol, game_config)
        self.num_cols = game_config['num_cols']
        self.num_rows = game_config['num_rows']
        self.win_n = game_config['win_n']
        
    def find_available_moves(self, board):
        return [col for col in range(self.num_cols) if any(board[row][col] == 0 for row in range(self.num_rows))]
    
    def get_move(self, board):
        return random.choice(self.find_available_moves(board))