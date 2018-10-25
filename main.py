"""This is the main script to run the simulation."""

import pygame
import constants
from copy import deepcopy
import json
from system import System
from message import BaseMessage
import agentstate
from make_csv import MakeCsv
from tqdm import tqdm

DISPLAY = False

SYSTEM = System(DISPLAY)
n_simulations = 25

for i in range(n_simulations):
    print("Simulation {0}/{1}".format(i+1, n_simulations))

    # Create agents
    for agent_idx in range(constants.N_AGENTS):
        SYSTEM.create_agent(name="Agent_{}".format(agent_idx),
                            agent_id=agent_idx,
                            no_agents=constants.N_AGENTS)

    SYSTEM.initialize_total_negotiations_count()

    for i in tqdm(range(constants.MAX_TIME)):
        for name, agent in SYSTEM.agents.items():
            if isinstance(agent.state, agentstate.RandomWalkState):
                from dmp import DecisionMakingProcess
                dmp = DecisionMakingProcess(agent)
                decision = dmp.make_decision()

                if decision:
                    agent.state = agentstate.WalkToAgentState(
                        this_agent=agent,
                        other_agent=decision.performed_on_agent,
                        action_to_perform=decision)

        if SYSTEM.advance():
            print("Aborted system!")
            break

    pygame.quit()

    MakeCsv().make_csv(
        all_agents=[deepcopy(agent) for _, agent in SYSTEM.agents.items()],
        sort_by='Earnings')

quit()
