GAME_CONFIG=configs/easy.json
AGENT1=my_agent
# AGENT1=human # set AGENT1 as "human" to play the game yourself
AGENT2=baselines.baseline1

python main.py --config_path $GAME_CONFIG \
                --agent1 $AGENT1 \
                --agent2 $AGENT2 \
                --interactive