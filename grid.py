import sys
from random import randint


class Agent():
    def __init__(self, x, y, agent_id):
        self.x = x
        self.y = y
        self.agent_id = agent_id

    def get_id(self):
        return str(self.agent_id)


class AllAgents():
    agents = []

    def __init__(self, width, height, no_agents):
        for i in range(no_agents):
            x = randint(0, width-1)
            y = randint(0, height-1)
            id = randint(0, 1000)

            self.agents.append(Agent(x, y, id))

    def agent_at(self, x, y):
        for a in self.agents:
            if a.x == x and a.y == y:
                return True
        return False


class Tile():
    def __init__(self):
        self.containsAgent = False

    def set_tile(self, has_agent):
        self.containsAgent = has_agent


class Grid():
    def __init__(self, width, height, agents):
        self.width = width
        self.height = height
        self.grid = [[Tile()] * width for i in range(height)]

    def set_tiles(self, agents):
        for y in range(self.height):
            for x in range(self.width):
                if agents.agent_at(x, y):
                    self.grid[y][x].set_tile(True)
                else:
                    self.grid[y][x].set_tile(False)



    def print_grid(self, agents):
        for y in range(self.height):
            for x in range(self.width):
                if agents.agent_at(x, y):
                    print("0", end="")
                else:
                    print("_", end="")
            print("")


def main(argv):
    width = 50
    height = 20
    no_agents = 30
    agents = AllAgents(width, height, no_agents)
    grid = Grid(width, height, agents)  # width, height

    grid.set_tiles(agents)

    print("")

    grid.print_grid(agents)


if __name__ == "__main__":
    main(sys.argv)