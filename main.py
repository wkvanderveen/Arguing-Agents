"""Docstring for main.py"""

from system import System
from message import BaseMessage
from grid import *
from agentstate import *
from random import random


display = True
SYSTEM = System(display)

# Create agents
for agent_idx in range(constants.N_AGENTS):
    SYSTEM.create_agent(name="Agent_{}".format(agent_idx),
                        agent_id=agent_idx,
                        no_agents=constants.N_AGENTS)


for i in range(constants.MAX_TIME):
    print("\nUpdating system...\n{}\n".format('-' * 56))
    SYSTEM.print_info()

    ### HARDCODED SEND REQUEST between adjacent agents

    for name, agent in SYSTEM.agents.items():
        if random() < 0.005 :
            if isinstance(agent.state, RandomWalkState):
                agent.state = WalkToAgentState(this_agent=agent, other_agent=SYSTEM.get_random_target(agent.agent_id))

    ###

    if SYSTEM.advance():
        print("Aborted system!")
        break

pygame.quit()
quit()
