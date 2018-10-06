import constants
from random import randint, shuffle
from agent import Agent


class GridModel(object):

    def __init__(self):
        self.agents = []

    #TODO Remove this function (just for testing purposes)
    def set_following_agent(self):
        self.agents[0].set_target(self.agents[1])
        self.agents[0].current_activity = constants.SEARCH_AGENT

    def update(self):
        indices = list(range(len(self.agents)))
        shuffle(indices)
        for index in indices:  # update agents in random order
            agent = self.agents[index]
            agent.set_neighbors(self.check_neighbors(agent))
            agent.update()

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

    def add_agent(self, id, no_agents):
        x = randint(0, constants.TILES_X - 1)
        y = randint(0, constants.TILES_Y - 1)
        self.agents.append(Agent(x, y, id, no_agents))

