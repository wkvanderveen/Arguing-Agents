from random import randint
from random import random
from basket import Basket
import constants


class Agent():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.money = constants.MONEY
        self.elasticity = random()  # more elasticity --> accepting lower price
        self.patience = randint(0, constants.MAXPATIENCE)  # More patience --> more negotiation steps
        self.basket = Basket()

        self.encounters = []

    # TODO: In this function negotiation about a price should take place
    def negotiate(self):
        for trade_partner in self.encounters:
            pass

    def update(self):
        # TODO: think about other walking methods than random walk (seek other agent, avoid agents, etc.)
        self.random_walk()

    def random_walk(self):
        dx, dy = self.movement(randint(0, 3))
        while (self.x + dx) < 0 or (self.x + dx) >= constants.TILES_X or (self.y + dy) < 0 or \
                        (self.y + dy) >= constants.TILES_Y:
            dx, dy = self.movement(randint(0, 3))
        self.x = self.x + dx
        self.y = self.y + dy

    def set_encounters(self, agent):
        self.encounters.append(agent)

    def reset_encounters(self):
        self.encounters = []

    def no_encounters(self):
        return len(self.encounters)

    @staticmethod
    def movement(direction):
        if direction == 0:  # NORTH
            return 0, -1
        elif direction == 1:  # EAST
            return 1, 0
        elif direction == 2:  # SOUTH
            return 0, 1
        else:  # WEST
            return -1, 0

