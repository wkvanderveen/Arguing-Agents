"""docstring placeholder"""
from agent import *
import pygame
from gridmodel import GridModel
from gridview import GridView
from gridcontrol import GridControl
import constants
from random import choice, shuffle
import time

class System():
    """docstring for System"""

    def __init__(self, display):
        self.time = 0
        self.agents = dict()
        self.display = display

        self.model = GridModel()

        if display:
            pygame.init()
            pygame.display.set_caption("Grid with agents")
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


        requests_sent = 0
        requests_received = 0

        responses_sent = 0
        responses_received = 0

        items = list(self.agents.items())
        shuffle(items)

        # Let all agents send their messages
        print("\nSENDING MESSAGES:")
        for name, agent in items:
            agent.send_requests()
            responses_sent += agent.send_responses()

        # Let all agents receive messages
        print("\nRECEIVING MESSAGES:")
        for name, agent in items:
            requests_received += agent.receive_requests()
            responses_received += agent.receive_responses()

        print("\nAGENT INFO:")
        for name, agent in items:
            agent.set_neighbors(self.get_neighbors(agent))
            print("incoming: " + str(agent.has_incoming_messages()))
            if isinstance(agent.state, NegotiationState):
                # TODO: negotiate process
                agent.state.duration += 1

            elif isinstance(agent.state, RandomWalkState):
                agent.random_walk()

            elif isinstance(agent.state, WalkToAgentState):
                agent.search_agent(self.find_path(agent))

            elif isinstance(agent.state, WaitForResponseState):
                if agent.state.counter <= 0:
                    agent.state = RandomWalkState(this_agent=agent)
                else:
                    agent.state.counter = agent.state.counter - 1

        for name, agent in self.agents.items():
            agent.set_color()
            agent.state.print_info()

        self.time += 1

        self.model.update()
        closed = False

        # draw screen
        if self.display:
            self.view.draw()

            # update
            pygame.display.update()
            time.sleep(0.2)
            closed = self.control.check_events()

        return closed

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

    def agent_at(self, x, y):
        for name, agent in self.agents.items():
            if agent.x == x and agent.y == y:
                return agent
        return None

    def find_path(self, agent):
        target = agent.state.other_agent
        distances = [constants.INF, constants.INF, constants.INF, constants.INF]  # [north, east, south, west]
        directions = []

        distances[constants.NORTH] = self.bfs((agent.x, agent.y - 1), (target.x, target.y))
        distances[constants.EAST] = self.bfs((agent.x + 1, agent.y), (target.x, target.y))
        distances[constants.SOUTH] = self.bfs((agent.x, agent.y + 1), (target.x, target.y))
        distances[constants.WEST] = self.bfs((agent.x - 1, agent.y), (target.x, target.y))

        min_dist = min(distances)

        if min_dist == constants.INF:
            return directions

        if distances[constants.NORTH] == min_dist: directions.append(constants.NORTH)
        if distances[constants.EAST] == min_dist: directions.append(constants.EAST)
        if distances[constants.SOUTH] == min_dist: directions.append(constants.SOUTH)
        if distances[constants.WEST] == min_dist: directions.append(constants.WEST)

        return directions

    def bfs(self, start, end):
        explored = []
        queue = [start]
        levels = {}
        levels[start] = 0
        visited = [start]

        while queue:
            pos = queue.pop(0)
            x = pos[0]
            y = pos[1]
            explored.append(pos)
            neighbors = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
            for neighbor in neighbors:
                if neighbor[0] < 0 or neighbor[0] >= constants.TILES_X or neighbor[1] < 0 or neighbor[1] \
                        >= constants.TILES_Y:
                    continue
                if self.agent_at(neighbor[0], neighbor[1]) and not neighbor == end:
                    continue
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.append(neighbor)

                    levels[neighbor] = levels[pos] + 1

        if end not in levels:  # not a single step could have been taken (impossible position)
            return constants.INF
        return levels[end]

    def get_random_target(self, agent_id):
        name, target = choice(list(self.agents.items()))
        while target.agent_id == agent_id:
            name, target = choice(list(self.agents.items()))
        return target

    def print_info(self):
        """Print the information about the system."""
        print("Time = {0}.\nNumber of agents = {1}.\n".format(
            self.time, len(self.agents)))
