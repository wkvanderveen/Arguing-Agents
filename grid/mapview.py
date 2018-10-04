import pygame
import constants

from mapmodel import MapModel

class MapView(object):

    FONTSIZE = 20
    BACKGROUNDCOLOR = (255,255,255)

    def __init__(self, model):
        self.model = model
        self.screen = pygame.display.set_mode((constants.MAPWIDTH, constants.MAPHEIGHT))
        pygame.font.init()
        self.font = pygame.font.SysFont('fontawesome5free',
                                        MapView.FONTSIZE)

    def draw(self):
        self.drawBack()

        if self.model.center == -1:
            self.drawMain()
        else:
            self.drawCenter()

    def drawBack(self):
        self.screen.fill(MapView.BACKGROUNDCOLOR)

    def drawMain(self):
        for idx in range(len(self.model.centers)):
            color = constants.CENTERPROPS[idx][0]
            pos = constants.CENTERPROPS[idx][1]
            pygame.draw.circle(self.screen, color, pos,
                               constants.CENTERRADIUS)
            textsurface = self.font.render(self.model.centers[idx], False, (0, 0, 0))
            self.screen.blit(textsurface, (pos[0]-constants.CENTERRADIUS+10, pos[1]-(MapView.FONTSIZE/2)))

    def drawCenter(self):
        y_pos = constants.RECTDIST
        while y_pos < constants.MAPHEIGHT:
            x_pos = constants.RECTDIST
            while x_pos < constants.MAPWIDTH:
                pygame.draw.rect(self.screen, constants.blue,
                                 (x_pos, y_pos, constants.RECTSIZE,
                                  constants.RECTSIZE))
                x_pos += constants.RECTSIZE + constants.RECTDIST
            y_pos += constants.RECTSIZE + constants.RECTDIST

        cars = self.model.cars[self.model.center]

        for car in cars:
            color = constants.black
            if not car.isAvailable:
                color = constants.darkred
            pygame.draw.circle(self.screen, color,
                               MapView.getMapPos(car.pos[0] + car.distance[0],
                                                 car.pos[1] + car.distance[1]),
                               int(constants.RECTDIST / 2))

        clients = self.model.clients[self.model.center]

        for client in clients:
            if client[4]:
                pygame.draw.circle(self.screen, constants.red,
                                   MapView.getMapPos(client[0], client[1]),
                                   int(constants.RECTDIST / 2))

            pygame.draw.circle(self.screen, constants.green,
                               MapView.getMapPos(client[2], client[3]),
                               int(constants.RECTDIST / 2))
    @staticmethod
    def getMapPos(x, y):
        return (int(x * (constants.RECTSIZE + constants.RECTDIST) +
                    constants.RECTDIST * 0.5),
                int(y * (constants.RECTSIZE + constants.RECTDIST) +
                    constants.RECTDIST * 0.5))
