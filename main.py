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
import constants
from tqdm import tqdm


agents_at_end = []
display = True

SYSTEM = System(display)

# Create agents
for agent_idx in range(constants.N_AGENTS):
    SYSTEM.create_agent(name="Agent_{}".format(agent_idx),
                        agent_id=agent_idx,
                        no_agents=constants.N_AGENTS)

SYSTEM.initialize_total_negotiations_count()

agents_at_start = copy.deepcopy(SYSTEM.agents)

for i in tqdm(range(constants.MAX_TIME)):
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

for name, agent in SYSTEM.agents.items():
    agents_at_end.append(copy.deepcopy(agent))

pygame.quit()

MakeCsv().make_csv(agents_at_end, sort_by='Earnings')
quit()

