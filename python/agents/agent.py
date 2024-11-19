"""
    You should not modify this file. 
"""

class AgentBase:
    """
    Abstract base class for game agents.

    Attributes:
        name (str): The name of the agent.
        symbol (str): The symbol representing the agent (e.g., -1 or 1).
        game_config (dict): Configuration settings for the game.
    """

    def __init__(self, name, symbol, game_config):
        """
        Initializes an agent with a name, symbol, and game configuration.

        Args:
            name (str): The name of the agent.
            symbol (str): The symbol representing the agent.
            game_config (dict): The configuration settings for the game.
        """
        self._name = name
        self._symbol = symbol
        self._game_config = game_config

    def get_move(self, board):
        """
        Abstract method to determine the next move for the agent.

        Args:
            board (Board): The current game board.

        Returns:
            int: The column index where the agent wants to place its move.

        Raises:
            NotImplementedError: This method must be overridden in derived classes.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @property
    def game_config(self) -> dict:
        """Gets the game configuration settings."""
        return self._game_config

    @property
    def name(self) -> str:
        """Gets the name of the agent."""
        return self._name

    @property
    def symbol(self) -> str:
        """Gets the symbol representing the agent."""
        return self._symbol