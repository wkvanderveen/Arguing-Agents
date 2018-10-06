from random import randint
from random import random
from basket import Basket
import constants


class Agent():

    def __init__(self, x, y, agent_id):
        self.x = x
        self.y = y
        self.agent_id = agent_id
        self.money = constants.MONEY
        self.elasticity = random()  # more elasticity --> accepting lower price
        self.patience = randint(0, constants.MAXPATIENCE)  # More patience --> more negotiation steps
        self.basket = Basket()

        self.neighbors = [None, None, None, None]

    # TODO: In this function negotiation about a price should take place
    def negotiate(self):
        for trade_partner in self.encounters:
            pass

    def update(self):
        # TODO: think about other walking methods than random walk (seek other agent, avoid agents, etc.)
        self.random_walk()

    def random_walk(self):
        if self.enclosed():
            return False
        direction = randint(0, 3)
        while self.cannot_move(direction):
            direction = randint(0, 3)
        dx, dy = self.movement(direction)
        self.x = self.x + dx
        self.y = self.y + dy
        return True

    def enclosed(self):
        no_dirs = 4
        for direction in range(4):
            if self.cannot_move(direction):
                no_dirs = no_dirs - 1

        return True if no_dirs == 0 else False

    def cannot_move(self, direction):
        dx, dy = self.movement(direction)
        if (self.x + dx) < 0 or (self.x + dx) >= constants.TILES_X or (self.y + dy) < 0 or (self.y + dy)\
                >= constants.TILES_Y or not self.neighbors[direction] is None:
            return True
        return False

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def set_encounters(self, agent):
        self.encounters.append(agent)

    def reset_encounters(self):
        self.encounters = []

    def no_encounters(self):
        return len(self.encounters)

    def get_id(self):
        return self.agent_id

    @staticmethod
    def movement(direction):
        if direction == constants.NORTH:  # NORTH
            return 0, -1
        elif direction == constants.EAST:  # EAST
            return 1, 0
        elif direction == constants.SOUTH:  # SOUTH
            return 0, 1
        else:  # (3) WEST
            return -1, 0

