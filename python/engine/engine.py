import random
from copy import deepcopy
from engine.board import Board


class Engine:
    """
    A class to represent the game engine that manages gameplay between two players.

    Attributes:
        board (Board): The game board instance.
        player1 (Player): The first player instance.
        player2 (Player): The second player instance.
        __do_visualize (bool): Flag to enable or disable visualizing the game board.

    Methods:
        play(seed: int) -> str:
            Runs the game using the given seed for random number generation.
            Returns the name of the winning player or None if there's a tie.
    """

    def __init__(self, config, player1, player2, do_visualize=False):
        """
        Initialize the game engine with configuration, players, and visualization flag.

        Args:
            config (dict): Configuration settings for the game.
            player1 (Player): The first player.
            player2 (Player): The second player.
            do_visualize (bool): Whether to visualize the game board during play. Defaults to False.
        """
        self.board = Board(config)
        self.player1 = player1
        self.player2 = player2
        self.__do_visualize = do_visualize

    def play(self, seed: int) -> str:
        """
        Execute the game play by alternating turns between two players.

        Args:
            seed (int): The seed value for random number generators to ensure reproducibility.

        Returns:
            str: The name of the winning player, or None if the game ends in a tie.
        """
        random.seed(seed)

        if self.__do_visualize:
            self.board.visualize()

        current_player = self.player1

        while not self.board.is_full():
            board_copy = deepcopy(self.board.board)
            move = current_player.get_move(board_copy)
            print(f"{current_player.name} makes move: {move}")

            move_is_valid = self.board.update(move, current_player.symbol)

            if self.__do_visualize:
                self.board.visualize()

            if not move_is_valid:
                print(f"Invalid move made by {current_player.name}.")

                # Switch to the other player and return their name as the winner
                return self._switch_player(current_player).name

            if self.board.is_winner(current_player.symbol):
                return current_player.name

            # Switch to the other player
            current_player = self._switch_player(current_player)

        return None

    def _switch_player(self, current_player):
        """
        Switch the active player.

        Args:
            current_player (Player): The current player instance.

        Returns:
            Player: The next player instance.
        """
        return self.player2 if current_player == self.player1 else self.player1
