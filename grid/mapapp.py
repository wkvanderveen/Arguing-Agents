#!/usr/bin/env python
import pygame
from random import randint

from gridmodel import GridModel
from gridview import GridView
from gridcontrol import GridControl
import constants


class Grid(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Grid with agents')
        self.model = GridModel()
        self.view = GridView(self.model)
        self.control = GridControl(self.model)

    def start_loop(self):
        clock = pygame.time.Clock()
        crashed = False
        no_agents = 10

        for i in range(no_agents):
            x = randint(0, constants.TILES_X-1)
            y = randint(0, constants.TILES_Y-1)

            self.model.add_agent(x, y)

        while not crashed:
            #handle input
            crashed = self.control.checkEvents()

            self.model.update()

            #draw screen
            self.view.draw()

            #update
            pygame.display.update()
            clock.tick(3)


def main():
    grid = Grid()
    grid.start_loop()
    pygame.quit()
    quit()


if __name__== "__main__":
    main()
