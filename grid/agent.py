from random import randint
import constants


class Agent():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.random_walk()

    def random_walk(self):
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        while (self.x + dx) < 0 or (self.x + dx) >= constants.TILES_X or (self.y + dy) < 0 or \
                        (self.y + dy) >= constants.TILES_Y:
            dx = randint(-1, 1)
            dy = randint(-1, 1)
        self.x = self.x + dx
        self.y = self.y + dy
