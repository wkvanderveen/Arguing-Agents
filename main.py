"""Docstring for main.py"""

from system import System
from message.message import Message

SYSTEM = System()

SYSTEM.advance()

SYSTEM.create_agent("union",
                    [],
                    [],
                    [],
                    [(30, ("wage.increase", True)),
                     (None, ("unemployment", False))]
                   )

SYSTEM.advance()

SYSTEM.create_agent("management",
                    [],
                    [],
                    [],
                    [(None, ("save", True))])

SYSTEM.advance()

SYSTEM.agents["union"].outgoing_messages.append(Message(time=SYSTEM.time,
                                                        message_type="Request",
                                                        sender="union"))

SYSTEM.advance()

SYSTEM.agents["union"].print_info()

SYSTEM.advance()
