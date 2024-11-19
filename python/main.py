import json
import argparse
from utils import load_agent
from engine.engine import Engine
from engine.chessboard import Chessboard

"""
    You should not modify this file. 
"""
def main(config_path, agent1_name, agent2_name, interactive):
    # Load configuration from the specified JSON file
    with open(config_path) as f:
        config = json.load(f)

    # Dynamically load agents using the specified paths/names
    player1 = load_agent(agent1_name, config, 1)
    player2 = load_agent(agent2_name, config, -1)

    if not interactive:
        if player1 is None and player2 is None:
            raise Exception("Agent(s) Not Exist")

        # Create and run the game engine
        engine = Engine(config, player1, player2, do_visualize=True)
        winner = engine.play(args.seed)
        print(f"{winner} wins!" if winner else "It's a tie!")
    else:
        human_play = True if agent1_name == 'human' or agent2_name == 'human' else False
        human_symbol = 1 if agent1_name == 'human' else -1
        if player1 is None:
            player1, player2 = player2, player1
        if (not human_play) and (player1 is None or player2 is None):
            raise Exception("Agent(s) Not Exist")
        playground = Chessboard(config, player1, player2, human_play, human_symbol)
        playground.start()

if __name__ == "__main__":
    # Define argument parser
    parser = argparse.ArgumentParser(description="Game Engine Runner")
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--config_path', type=str, required=True, help="Path to the JSON config file")
    parser.add_argument('--agent1_name', type=str, required=True, help="Path for the first agent module (player1)")
    parser.add_argument('--agent2_name', type=str, required=True, help="Path for the second agent module (player2)")
    parser.add_argument('--interactive', action='store_true', default=False, help="Play in interactive mode")
    
    # Parse the arguments
    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.config_path, args.agent1_name, args.agent2_name, args.interactive)