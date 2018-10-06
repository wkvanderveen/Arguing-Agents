#!/usr/bin/env python
import pygame
from random import randint

from gridmodel import GridModel
from gridview import GridView
from gridcontrol import GridControl
import constants


class Parameters():
    def __init__(self):
        self.no_agents = min(int(input("Number of agents = ")), constants.TILES_X * constants.TILES_Y - 1)
        self.updates = min(int(input("Updates per second = ")), constants.MAX_UPDATES_PER_S)


class Grid():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Grid with agents")
        self.model = GridModel()
        self.view = GridView(self.model)
        self.control = GridControl(self.model)

    def start_loop(self, parameters):
        clock = pygame.time.Clock()
        crashed = False

        timestep = 0
        while not crashed:
            timestep = timestep + 1
            print("t = " + str(timestep))
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
