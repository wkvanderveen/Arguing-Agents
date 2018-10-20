"""Docstring for main.py"""

from random import random
import pygame
import constants
import copy
import json
from system import System
from message import BaseMessage
from grid import *
from agentstate import *
from make_csv import MakeCsv

display = True
SYSTEM = System(display)

# Create agents
for agent_idx in range(constants.N_AGENTS):
    SYSTEM.create_agent(name="Agent_{}".format(agent_idx),
                        agent_id=agent_idx,
                        no_agents=constants.N_AGENTS)

SYSTEM.initialize_total_negotiations_count()

agents_at_start = copy.deepcopy(SYSTEM.agents)

for i in range(constants.MAX_TIME):
    print("\nUpdating system...\n{}\n".format('-' * 56))
    SYSTEM.print_info()

    for name, agent in SYSTEM.agents.items():
        if isinstance(agent.state, RandomWalkState):
            from dmp import DecisionMakingProcess
            dmp = DecisionMakingProcess(agent)
            decision = dmp.make_decision()

            if decision:
                agent.state = WalkToAgentState(
                    this_agent=agent,
                    other_agent=decision.performed_on_agent,
                    action_to_perform=decision)

    if SYSTEM.advance():
        print("Aborted system!")
        break

agents_at_end = copy.deepcopy(SYSTEM.agents)

MakeCsv().make_csv()
pygame.quit()
quit()
