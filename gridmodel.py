import constants
from random import randint, shuffle
from agent import Agent


class GridModel(object):

    def __init__(self):
        self.agents = []

    def update(self):
        indices = list(range(len(self.agents)))
        shuffle(indices)
        for index in indices:  # update agents in random order
            agent = self.agents[index]
            agent.set_neighbors(self.check_neighbors(agent.x, agent.y))
            if agent.current_activity == constants.SEARCH_AGENT:
                agent.set_dir(self.find_path(agent))
            agent.update(self.get_random_target(index))

    def get_random_target(self, agent_idx):
        target_idx = randint(0, (len(self.agents) - 1))
        while target_idx == agent_idx:
            target_idx = randint(0, (len(self.agents) - 1))
        return self.agents[target_idx]

    def check_neighbors(self, x, y):
        dirs = [None, None, None, None]
        dirs[constants.NORTH] = self.agent_at(x, y - 1)
        dirs[constants.EAST] = self.agent_at(x + 1, y)
        dirs[constants.SOUTH] = self.agent_at(x, y + 1)
        dirs[constants.WEST] = self.agent_at(x - 1, y)
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

    def find_path(self, agent):
        start = (agent.x, agent.y)
        end = (agent.target_agent.x, agent.target_agent.y)

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
            neighbours = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
            for neighbour in neighbours:
                if neighbour[0] < 0 or neighbour[0] >= constants.TILES_X or neighbour[1] < 0 or neighbour[1] \
                        >= constants.TILES_Y:
                    continue
                if self.agent_at(neighbour[0], neighbour[1]) and not neighbour == end:
                    continue
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.append(neighbour)

                    levels[neighbour] = levels[pos] + 1

        print(levels[start])
        print(levels[end])



