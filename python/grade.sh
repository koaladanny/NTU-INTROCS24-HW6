GAME_CONFIG=configs/easy.json
TEST_AGENT=my_agent # this should be the agent you want to test (this should map the folder name in agents/ folder)
BASELINE=baselines.baseline1 # this is the baseline agent you want to compare with

python grade.py --config_path $GAME_CONFIG \
                --agent1 $TEST_AGENT \
                --agent2 $BASELINE \
                --run_episodes 100