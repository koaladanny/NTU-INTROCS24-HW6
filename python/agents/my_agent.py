# 4o : 98/72
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

    def update_board(self, board, col, symbol):
        new_board = deepcopy(board)
        for row in range(self.num_rows - 1, -1, -1):
            if new_board[row][col] == 0:
                new_board[row][col] = symbol
                return new_board
        return new_board

    def is_winner(self, board, symbol):
        for row in range(self.num_rows):
            for col in range(self.num_cols - self.win_n + 1):
                if all(board[row][col + i] == symbol for i in range(self.win_n)):
                    return True
        for row in range(self.num_rows - self.win_n + 1):
            for col in range(self.num_cols):
                if all(board[row + i][col] == symbol for i in range(self.win_n)):
                    return True
        for row in range(self.num_rows - self.win_n + 1):
            for col in range(self.num_cols - self.win_n + 1):
                if all(board[row + i][col + i] == symbol for i in range(self.win_n)):
                    return True
                if all(board[row + i][col + self.win_n - i - 1] == symbol for i in range(self.win_n)):
                    return True
        return False

    def evaluate_board(self, board, symbol):
        opponent_symbol = 3 - symbol
        score = 0

        # Scoring logic for potential winning lines
        def score_line(line):
            count_self = line.count(symbol)
            count_opponent = line.count(opponent_symbol)
            if count_self > 0 and count_opponent == 0:
                return count_self ** 2
            elif count_opponent > 0 and count_self == 0:
                return -(count_opponent ** 2)  # Penalize opponent threats
            return 0

        for row in range(self.num_rows):
            for col in range(self.num_cols - self.win_n + 1):
                line = [board[row][col + i] for i in range(self.win_n)]
                score += score_line(line)
        for row in range(self.num_rows - self.win_n + 1):
            for col in range(self.num_cols):
                line = [board[row + i][col] for i in range(self.win_n)]
                score += score_line(line)
        for row in range(self.num_rows - self.win_n + 1):
            for col in range(self.num_cols - self.win_n + 1):
                diag1 = [board[row + i][col + i] for i in range(self.win_n)]
                diag2 = [board[row + i][col + self.win_n - i - 1] for i in range(self.win_n)]
                score += score_line(diag1)
                score += score_line(diag2)

        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        moves = self.find_available_moves(board)
        if depth == 0 or not moves:
            return self.evaluate_board(board, self._symbol)

        if maximizing_player:
            max_eval = float('-inf')
            for col in moves:
                new_board = self.update_board(board, col, self._symbol)
                if self.is_winner(new_board, self._symbol):
                    return float('inf')
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent_symbol = 3 - self._symbol
            for col in moves:
                new_board = self.update_board(board, col, opponent_symbol)
                if self.is_winner(new_board, opponent_symbol):
                    return float('-inf')
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_move(self, board):
        moves = self.find_available_moves(board)
        best_score = float('-inf')
        best_move = None

        for col in moves:
            new_board = self.update_board(board, col, self._symbol)
            if self.is_winner(new_board, self._symbol):
                return col
            score = self.minimax(new_board, 2, float('-inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = col

        return best_move if best_move is not None else random.choice(moves)