"""Docstring for main.py"""

from system.system import System
from message.message import RequestMessage
from wff.wff import Wff
SYSTEM = System()

# Create agents 'Alice' and 'Bob'
SYSTEM.create_agent(name="Alice",
                    beliefs=[],
                    desires=[],
                    intentions=[],
                    goals=[])

SYSTEM.create_agent(name="Bob",
                    beliefs=[],
                    desires=[],
                    intentions=[],
                    goals=[])

mywff = Wff(wff_type='term_compare', terms=[2, 5])
print(mywff.convert_to_string())

# Alice sends a Request to Bob
SYSTEM.agents["Alice"].generate_message(time=SYSTEM.time,
                                        type_of_message='REQUEST',
                                        recipient=SYSTEM.agents["Bob"],
                                        sentence=mywff)

SYSTEM.agents["Alice"].print_info()


mypredwff = Wff(wff_type='predicate', times=[2], predicate=['P', ['x1', 'x2', 'x3']])
print(mypredwff.convert_to_string())


mynotwff = Wff(wff_type='not', wffs=[mypredwff])
print(mynotwff.convert_to_string())

myexistswff = Wff(wff_type='exists', wffs=[mynotwff], terms=['x'])
print(myexistswff.convert_to_string())

mymessagewff = Wff(wff_type='with_message',
                   times=[3],
                   send_receive='Send',
                   agents=[SYSTEM.agents["Alice"], SYSTEM.agents["Bob"]],
                   message=SYSTEM.agents["Alice"].outgoing_messages[0])
print(mymessagewff.convert_to_string())
