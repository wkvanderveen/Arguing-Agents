"""Docstring for main.py"""

from system import System
from message import BaseMessage
from grid import *
from agentstate import *
SYSTEM = System()

# Create agents
n_agents = 10
for agent_idx in range(n_agents):
    SYSTEM.create_agent(name="Agent_{}".format(agent_idx),
                        agent_id=agent_idx,
                        no_agents=n_agents)

for i in range(50):
    print("time = {}".format(SYSTEM.time))

    for name, agent in SYSTEM.agents.items():
        agent.state.print_info()

    ### HARDCODED SEND REQUEST between adjacent agents

    for name, agent in SYSTEM.agents.items():
        for name_other, agent_other in SYSTEM.agents.items():
            if agent.adjacent_to_agent(agent_other) and \
                isinstance(agent.state, RandomWalkState) and \
                isinstance(agent_other.state, RandomWalkState):
                agent.generate_request(request_type='buy',
                    receiver=agent_other,
                    fruit='mango',
                    quantity=100)

    ###

    if SYSTEM.advance():
        print("Aborted system!")
        break

pygame.quit()
quit()
