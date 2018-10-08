"""docstring placeholder"""
from agent import *
import pygame
from gridmodel import GridModel
from gridview import GridView
from gridcontrol import GridControl
import constants
import time

class System():
    """docstring for System"""

    def __init__(self):
        self.time = 0
        self.agents = dict()

        pygame.init()
        pygame.display.set_caption("Grid with agents")
        self.model = GridModel()
        self.view = GridView(self)
        self.control = GridControl(self.model)

        print("System initialized.")

    def create_agent(self, name, agent_id, no_agents, x=None, y=None):
        """Create a new Agent in the system."""
        x = randint(0, constants.TILES_X-1) if x == None else x
        y = randint(0, constants.TILES_Y-1) if y == None else x
        new_agent = Agent(name=name,
                          agent_id=agent_id,
                          no_agents=no_agents,
                          x=x,
                          y=y)

        self.agents[name] = new_agent

    def advance(self):
        """Advance the time by a value of 1."""

        print("\nUpdating system...\n{}\n".format('-' * 56))

        requests_sent = 0
        requests_received = 0

        responses_sent = 0
        responses_received = 0

        # Let all agents send their messages
        for name, agent in self.agents.items():
            requests_sent += agent.send_requests()
            responses_sent += agent.send_responses()

        # Let all agents receive messages
        for name, agent in self.agents.items():
            requests_received += agent.receive_requests()
            responses_received += agent.receive_responses()

        for name, agent in self.agents.items():
            agent.set_neighbors(self.get_neighbors(agent))
            if isinstance(agent.state, NegotiationState):
                # TODO: negotiate process
                agent.state.duration += 1

            elif isinstance(agent.state, RandomWalkState):
                agent.random_walk()

            elif isinstance(agent.state, WalkToAgentState):
                agent.search_agent()

        for name, agent in self.agents.items():
            agent.set_color()

        self.time += 1

        # handle input
        crashed = self.control.check_events()

        self.model.update()

        # draw screen
        self.view.draw()

        # update
        pygame.display.update()
        time.sleep(0.2)
        return self.control.check_events()

    # set the neighbors of an agent (required for preventing agents from walking through each other)
    def get_neighbors(self, agent):
        neighbors = [None, None, None, None]  # [North, East, South, West]
        for name, possible_neighbor in self.agents.items():
            if possible_neighbor.x == agent.x and possible_neighbor.y == (agent.y - 1):
                neighbors[constants.NORTH] = possible_neighbor
            if possible_neighbor.x == (agent.x + 1) and possible_neighbor.y == agent.y:
                neighbors[constants.EAST] = possible_neighbor
            if possible_neighbor.x == agent.x and possible_neighbor.y == (agent.y + 1):
                neighbors[constants.SOUTH] = possible_neighbor
            if possible_neighbor.x == (agent.x - 1) and possible_neighbor.y == agent.y:
                neighbors[constants.WEST] = possible_neighbor
        return neighbors





    def print_info(self):
        """Print the information about the system."""
        print("Time = {0}.\nNumber of agents = {1}.\n".format(
            self.time, len(self.agents)))
