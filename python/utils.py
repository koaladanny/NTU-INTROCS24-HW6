import importlib

def load_agent(agent_name, config, symbol):
    """
    Dynamically import an agent class from the specified module path.
    Args:
        module_path (str): Path to the agent module.
        config (dict): Configuration for the game.
        symbol (str): Symbol for the player (-1 or 1).
        agent_name (str): Name of the agent to be imported.
    Returns:
        instance of the Agent class, `None` if agent does not exist.
    """
    try:
        module_name = f"agents.{agent_name}"
        agent_module = importlib.import_module(module_name)
        AgentClass = getattr(agent_module, "Agent")
        return AgentClass(agent_name, symbol, config)
    except:
        return None