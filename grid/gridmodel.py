import constants
from random import randint
from agent import Agent


class GridModel(object):

    def __init__(self):
        self.agents = []

    def update(self):
        self.reset_encounters()
        for agent in self.agents:
            agent.update()
        self.check_encounters()
        self.start_negotiation()

    def reset_encounters(self):
        for agent in self.agents:
            agent.reset_encounters()

    def check_encounters(self):
        no_agents = len(self.agents)
        for i in range(0, no_agents):
            for j in range(i+1, no_agents):
                if self.agents[i].x == self.agents[j].x and self.agents[i].y == self.agents[j].y:
                    self.agents[i].set_encounters(self.agents[j])
                    self.agents[j].set_encounters(self.agents[i])

    def start_negotiation(self):
        for agent in self.agents:
            agent.negotiate()

    def add_agent(self):
        x = randint(0, constants.TILES_X - 1)
        y = randint(0, constants.TILES_Y - 1)
        self.agents.append(Agent(x, y))

