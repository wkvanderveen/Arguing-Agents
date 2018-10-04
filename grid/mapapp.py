#!/usr/bin/env python
import pygame
from pygame.locals import *
from mapmodel import MapModel
from mapview import MapView
from mapcontrol import MapControl

class MapApp(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Map with cars')
        self.model = MapModel()
        self.view = MapView(self.model)
        self.control = MapControl(self.model)

        #test -----
        # self.model.addCenter(["test", "1", "localhost", "1111"])
        # self.model.addClient(["test", "1", "2", "4", "4"])
        # self.model.cars[0][0].goto("1,2,4,4")


    def start_loop(self):
        clock = pygame.time.Clock()
        crashed = False

        while not crashed:

            #handle input
            crashed = self.control.checkEvents()

            self.model.update()

            #draw screen
            self.view.draw()

            #update
            pygame.display.update()
            clock.tick(60)

def main():
    app = MapApp()
    app.start_loop()
    pygame.quit()
    quit()

if __name__== "__main__":
    main()
  
