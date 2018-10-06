"""Docstring for main.py"""

from system import System
from message import BaseMessage
from grid import *
SYSTEM = System()




# Create agents 'Alice' and 'Bob'
SYSTEM.create_agent(name="Bob", agent_id=0, no_agents=2, x=4, y=4)

SYSTEM.create_agent(name="Alice", agent_id=1, no_agents=2, x=7, y=7)
# Both agents are now in a RandomWalk state

for i in range(50):
    print(SYSTEM.time)
    SYSTEM.agents["Alice"].state.print_info()
    SYSTEM.agents["Bob"].state.print_info()
    if SYSTEM.advance():
        print("Aborted system!")
        break


# Alice has received the Yes response
# Both agents are now in a Negotiation state



pygame.quit()
quit()
