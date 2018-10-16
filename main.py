"""Docstring for main.py"""

from system import System
from message import BaseMessage
from grid import *
from agentstate import *
from random import random
import constants
import pygame
import copy
import json


display = True
SYSTEM = System(display)

# Create agents
for agent_idx in range(constants.N_AGENTS):
    SYSTEM.create_agent(name="Agent_{}".format(agent_idx),
                        agent_id=agent_idx,
                        no_agents=constants.N_AGENTS)



SYSTEM.initialize_total_negotiations_count()

agents_at_start=copy.deepcopy(SYSTEM.agents)




for i in range(constants.MAX_TIME):
    print("\nUpdating system...\n{}\n".format('-' * 56))
    SYSTEM.print_info()

    ### HARDCODED SEND REQUEST between adjacent agents

    # for name, agent in SYSTEM.agents.items():
    #     if random() < 0.005 :
    #         if isinstance(agent.state, RandomWalkState):
    #             agent.state = WalkToAgentState(this_agent=agent, other_agent=SYSTEM.get_random_target(agent.agent_id))

    for name,agent in SYSTEM.agents.items():
        if isinstance(agent.state, RandomWalkState):
            from dmp import DecisionMakingProcess
            dmp = DecisionMakingProcess(agent)
            decision = dmp.make_decision()

            if decision:
                agent.state = WalkToAgentState(this_agent=agent, other_agent=decision.performed_on_agent,action_to_perform=decision)


    ###

    if SYSTEM.advance():
        print("Aborted system!")
        break

agents_at_end=copy.deepcopy(SYSTEM.agents)

print("Agents At Start")
for n,a in agents_at_start.items():
    print(n,a.money,json.dumps(a.entities_info))

print("\n Agents At End")
for n,a in agents_at_end.items():
    print(n,a.money,json.dumps(a.entities_info))

pygame.quit()
quit()
