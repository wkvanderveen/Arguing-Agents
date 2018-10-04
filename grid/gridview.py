import pygame
import constants
from gridmodel import GridModel


class GridView(object):

    FONTSIZE = 20
    BACKGROUNDCOLOR = constants.WHITE

    def __init__(self, model):
        self.model = model
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.font.init()
        self.font = pygame.font.SysFont('fontawesome5free',self.FONTSIZE)

    def draw(self):
        self.draw_bg()
        self.draw_tiles()

    def draw_bg(self):
        self.screen.fill(self.BACKGROUNDCOLOR)

    def draw_tiles(self):
        y_pos = constants.RECTDIST
        while y_pos < constants.HEIGHT:
            x_pos = constants.RECTDIST
            while x_pos < constants.WIDTH:
                pygame.draw.rect(self.screen, constants.BLUE, (x_pos, y_pos, constants.RECTSIZE, constants.RECTSIZE))
                x_pos += constants.RECTSIZE + constants.RECTDIST
            y_pos += constants.RECTSIZE + constants.RECTDIST

        agents = self.model.agents

        for agent in agents:

            color = constants.BLACK

            pygame.draw.rect(self.screen, color, (self.get_grid_pos(agent.x, agent.y)[0],
                                                  self.get_grid_pos(agent.x, agent.y)[1], constants.RECTSIZE - 8,
                                                  constants.RECTSIZE - 8))

    @staticmethod
    def get_grid_pos(x, y):
        return int(x * (constants.RECTSIZE + constants.RECTDIST) + 5 * constants.RECTDIST), \
               int(y * (constants.RECTSIZE + constants.RECTDIST) + 5 * constants.RECTDIST)
