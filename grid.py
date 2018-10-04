import sys
from random import randint
import time


class Agent():
    def __init__(self, x, y, agent_id, width, height):
        self.x = x
        self.y = y
        self.agent_id = agent_id
        self.width = width
        self.height = height

    def get_id(self):
        return str(self.agent_id)

    def random_walk(self):
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        while (self.x + dx) < 0 or (self.x + dx) >= self.width or (self.y + dy) < 0 or (self.y + dy) >= self.height:
            dx = randint(-1, 1)
            dy = randint(-1, 1)
        self.x = self.x + dx
        self.y = self.y + dy


class AllAgents():
    agents = []

    def __init__(self, width, height, no_agents):
        for i in range(no_agents):
            x = randint(0, width-1)
            y = randint(0, height-1)
            agent_id = randint(0, 1000)

            self.agents.append(Agent(x, y, agent_id, width, height))

    def agent_at(self, x, y):
        no_agents = 0
        for a in self.agents:
            if a.x == x and a.y == y:
                no_agents = no_agents + 1
        return no_agents

    def update(self):
        for a in self.agents:
            a.random_walk()


class Tile():
    def __init__(self):
        self.no_agents = 0

    def set_tile(self, no_agents):
        self.no_agents = no_agents

    def agents_at(self):
        return self.no_agents


class Grid():
    def __init__(self, width, height, agents):
        self.width = width
        self.height = height
        # self.grid = [[Tile()] * width for i in range(height)]

        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Tile())
            self.grid.append(row)

    def set_tiles(self, agents):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].set_tile(agents.agent_at(x, y))

    def print_grid(self):

        for y in range(self.height):
            print("|", end="")
            for x in range(self.width):
                if self.grid[y][x].agents_at():
                    if self.grid[y][x].agents_at() < 10:
                        print(str(self.grid[y][x].agents_at()) + "  ", end="")
                    else:
                        print(str(self.grid[y][x].agents_at()) + " ", end="")
                else:
                    print("_  ", end="")
            print("|")
        print("-" * (self.width * 3 + 2))


def main(argv):
    epochs = 10
    width = 16
    height = 16
    no_agents = 4
    agents = AllAgents(width, height, no_agents)
    grid = Grid(width, height, agents)  # width, height

    for epoch in range(1, epochs+1):
        print("Epoch " + str(epoch))
        grid.set_tiles(agents)
        grid.print_grid()
        agents.update()
        time.sleep(1)


if __name__ == "__main__":
    main(sys.argv)