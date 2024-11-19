import json
import argparse
from utils import load_agent
from engine.engine import Engine

"""
    You should not modify this file. 
"""
def main(config_path, agent1_name, agent2_name, run_episodes):
    # Load configuration from the specified JSON file
    with open(config_path) as f:
        config = json.load(f)

    # Dynamically load agents using the specified paths/names
    player1 = load_agent(agent1_name, config, 1)
    player2 = load_agent(agent2_name, config, -1)

    stats = []

    # Create and run the game engine
    for seed in range(run_episodes):
        print(f"=====================Episode {seed + 1}=====================")
        if seed % 2 == 0:
            engine = Engine(config, player1, player2)
        else:
            engine = Engine(config, player2, player1)
        winner = engine.play(seed)

        score = 1 if winner == player1.name else 0 if winner == player2.name else 0.5
        stats.append(score)

        print(f"{winner} wins!" if winner else "It's a tie!")
    
    print(f"=====================Final Results=====================")
    final_score = int(sum(stats) / len(stats) * 100)
    print("Total score:", final_score)

if __name__ == "__main__":
    # Define argument parser
    parser = argparse.ArgumentParser(description="Game Engine Runner")
    parser.add_argument('--config_path', type=str, required=True, help="Path to the JSON config file")
    parser.add_argument('--agent1_name', type=str, required=True, help="Path for the first agent module (player1)")
    parser.add_argument('--agent2_name', type=str, required=True, help="Path for the second agent module (player2)")
    parser.add_argument('--run_episodes', type=int, required=True, help="Number of episodes to run")
    
    # Parse the arguments
    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.config_path, args.agent1_name, args.agent2_name, args.run_episodes)