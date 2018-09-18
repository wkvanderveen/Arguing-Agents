"""Docstring for main.py"""

from system.system import System
from message.message import RequestMessage

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

SYSTEM.agents["union"].generate_message(SYSTEM.time+1,'REQUEST',SYSTEM.agents["management"])

SYSTEM.advance()

SYSTEM.agents["union"].print_info()

SYSTEM.advance()
