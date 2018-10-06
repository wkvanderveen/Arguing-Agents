"""Docstring for main.py"""

from system import System
from message import BaseMessage
SYSTEM = System()



# Create agents 'Alice' and 'Bob'

SYSTEM.create_agent(name="Bob")

SYSTEM.create_agent(name="Alice")
# Both agents are now in a RandomWalk state

SYSTEM.agents["Alice"].generate_request(request_type='buy',
                                        receiver=SYSTEM.agents["Bob"],
                                        fruit='mango',
                                        quantity=100)

SYSTEM.advance()

# Alice has sent a Buy request to Bob
# Bob is receiving the message and is sending back a Yes response

SYSTEM.advance()

# Alice has received the Yes response
# Both agents are now in a Negotiation state

SYSTEM.agents["Alice"].state.print_info()

SYSTEM.agents["Bob"].state.print_info()
