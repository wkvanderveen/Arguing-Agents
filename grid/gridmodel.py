import constants
from random import randint, shuffle
from agent import Agent


class GridModel(object):

    def __init__(self):
        self.agents = []

    def update(self):
        self.reset_encounters()

        indices = list(range(len(self.agents)))
        shuffle(indices)
        for index in indices:  # update agents in random order
            agent = self.agents[index]
            agent.set_neighbors(self.check_neighbors(agent))
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

    def check_neighbors(self, agent):
        dirs = [None, None, None, None]
        dirs[constants.NORTH] = self.agent_at(agent.x, agent.y - 1)
        dirs[constants.EAST] = self.agent_at(agent.x + 1, agent.y)
        dirs[constants.SOUTH] = self.agent_at(agent.x, agent.y + 1)
        dirs[constants.WEST] = self.agent_at(agent.x - 1, agent.y)
        return dirs

    def agent_at(self, x, y):
        for agent in self.agents:
            if agent.x == x and agent.y == y:
                return agent
        return None

    def get_number_of_agents(self):
        return len(self.agents)

    def add_agent(self, id):
        x = randint(0, constants.TILES_X - 1)
        y = randint(0, constants.TILES_Y - 1)
        self.agents.append(Agent(x, y, id))

