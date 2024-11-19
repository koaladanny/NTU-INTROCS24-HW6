"""
    You should not modify this file. 
"""

class Board:
    """
    Represents a four-in-a-row game board.
    """
    
    def __init__(self, config):
        """
        Initializes the game board based on the configuration provided.

        Args:
            config (dict): A dictionary containing the number of columns, rows, and winning condition.
        """
        self.__num_cols = config['num_cols']
        self.__num_rows = config['num_rows']
        self.__win_n = config['win_n']
        self.__board = [[0 for _ in range(self.__num_cols)] for _ in range(self.__num_rows)]
    
    @property
    def num_cols(self):
        """Returns the number of columns in the board."""
        return self.__num_cols
    
    @property
    def num_rows(self):
        """Returns the number of rows in the board."""
        return self.__num_rows
    
    @property
    def win_n(self):
        """Returns the number of tokens in a row required to win."""
        return self.__win_n
    
    @property
    def board(self):
        """Returns the current state of the board."""
        return self.__board

    def __valid_move(self, col):
        """
        Checks if a move is valid for the specified column.

        Args:
            col (int): The column to check for validity.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if not (0 <= col < self.__num_cols):
            return False
        
        if all(self.__board[row][col] != 0 for row in range(self.__num_rows)):
            return False
        
        return True

    def update(self, col, player_symbol):
        """
        Updates the board with the player's move.

        Args:
            col (int): The column where the player wants to place their symbol.
            player_symbol (str): The symbol of the player (-1 or 1).

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if not self.__valid_move(col):
            return False
        
        for row in range(self.__num_rows-1, -1, -1):
            if self.__board[row][col] == 0:
                self.__board[row][col] = player_symbol
                return (row, col)

        return False

    def is_winner(self, player_symbol):
        """
        Checks if the specified player has won the game.

        Args:
            player_symbol (str): The symbol of the player to check for a win.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        # Check horizontal
        for row in range(self.__num_rows):
            for col in range(self.__num_cols - self.__win_n + 1):
                if all(self.__board[row][col + i] == player_symbol for i in range(self.__win_n)):
                    return True

        # Check vertical
        for row in range(self.__num_rows - self.__win_n + 1):
            for col in range(self.__num_cols):
                if all(self.__board[row + i][col] == player_symbol for i in range(self.__win_n)):
                    return True

        # Check diagonal
        for row in range(self.__num_rows - self.__win_n + 1):
            for col in range(self.__num_cols - self.__win_n + 1):
                if all(self.__board[row + i][col + i] == player_symbol for i in range(self.__win_n)):
                    return True

                if all(self.__board[row + i][col + self.__win_n - i - 1] == player_symbol for i in range(self.__win_n)):
                    return True

        return False
    
    def is_full(self):
        """
        Checks if the board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return all(self.__board[row][col] != 0 for row in range(self.__num_rows) for col in range(self.__num_cols))
    
    def visualize(self):
        """
        Visualizes the current state of the board.
        """
        print("\n".join([" ".join(row) for row in reversed(self.__board)]))
        print()