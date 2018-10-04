#!/usr/bin/env python
import pygame
from random import randint

from gridmodel import GridModel
from gridview import GridView
from gridcontrol import GridControl
import constants


class Parameters():
    def __init__(self):
        self.no_agents = int(input("Number of agents = "))
        self.updates = int(input("Updates per second = "))


class Grid():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Grid with agents')
        self.model = GridModel()
        self.view = GridView(self.model)
        self.control = GridControl(self.model)

    def start_loop(self, parameters):
        clock = pygame.time.Clock()
        crashed = False

        # Add agents
        for i in range(parameters.no_agents):
            self.model.add_agent()

        while not crashed:
            # handle input
            crashed = self.control.check_events()

            self.model.update()

            # draw screen
            self.view.draw()

            # update
            pygame.display.update()
            clock.tick(parameters.updates)


def main():
    parameters = Parameters()
    grid = Grid()
    grid.start_loop(parameters)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
