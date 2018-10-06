"""Docstring for main.py"""

from system import System
from message import BaseMessage
from grid import *
from agentstate import *
SYSTEM = System()

# Create agents 'Alice' and 'Bob'
SYSTEM.create_agent(name="Bob", agent_id=0, no_agents=2, x=0, y=0)

SYSTEM.create_agent(name="Alice", agent_id=1, no_agents=2, x=15, y=18)
# Both agents are now in a RandomWalk state

for i in range(50):
    print("time = {}".format(SYSTEM.time))
    SYSTEM.agents["Alice"].state.print_info()
    SYSTEM.agents["Bob"].state.print_info()

    SYSTEM.agents["Alice"].state = WalkToAgentState(this_agent=SYSTEM.agents["Alice"],
                                                    other_agent=SYSTEM.agents["Bob"])

    ### HARDCODED SEND REQUEST
    if (SYSTEM.agents["Bob"].adjacent_to_agent(SYSTEM.agents["Alice"])):
        SYSTEM.agents["Alice"].generate_request(request_type='buy',
                                                receiver=SYSTEM.agents["Bob"],
                                                fruit='mango',
                                                quantity=100)
    ###

    if SYSTEM.advance():
        print("Aborted system!")
        break

pygame.quit()
quit()
