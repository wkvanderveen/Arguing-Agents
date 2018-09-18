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

# Construct message from page 7
mysentence = Wff(wff_type='predicate',
                 times=["t1"],
                 agents=[SYSTEM.agents["Bob"]],
                 predicate=['Do', "let.use.printer"])

arg_pre_neg = Wff(wff_type='not', wffs=[mysentence])

arg_cons = Wff(wff_type='predicate',
               times=["t2"],
               agents=[SYSTEM.agents["Alice"]],
               predicate=['Do', "break.printer"])

myargument = Wff(wff_type='implies', wffs=[arg_pre_neg, arg_cons])

# Alice sends a Request to Bob
SYSTEM.agents["Alice"].generate_message(time=SYSTEM.time,
                                        type_of_message='REQUEST',
                                        recipient=SYSTEM.agents["Bob"],
                                        sentence=mysentence,
                                        argument=myargument)


print(SYSTEM.agents["Alice"].outgoing_messages[0].convert_to_string())
