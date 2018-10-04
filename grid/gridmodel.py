import math
import constants
from agent import Agent


class GridModel(object):

    def __init__(self):
        self.agents = []

    def update(self):
        for agent in self.agents:
            agent.update()

    def add_agent(self, x, y, agent_id):
        self.agents.append(Agent(x, y))


    @staticmethod
    def inCircle(click, point):
        return ((math.pow((click[0] - point[0]), 2)) +
                math.pow((click[1] - point[1]), 2) <
                pow(constants.CENTERRADIUS, 2))
