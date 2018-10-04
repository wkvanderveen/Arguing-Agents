import math
import constants
from agent import Agent


class GridModel(object):

    def __init__(self):
        self.agents = []

    def update(self):
        for agent in self.agents:
            agent.update()

    def add_agent(self, x, y):
        self.agents.append(Agent(x, y))

