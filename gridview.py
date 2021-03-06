import pygame
import constants


class GridView(object):

    FONTSIZE = 20
    BACKGROUNDCOLOR = constants.WHITE

    def __init__(self, system):
        self.system = system
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.font.init()
        self.font = pygame.font.SysFont('fontawesome5free',self.FONTSIZE)

    def draw(self):
        self.draw_bg()
        self.draw_tiles()
        self.draw_agents()

    def draw_bg(self):
        self.screen.fill(self.BACKGROUNDCOLOR)

    def draw_tiles(self):
        y_pos = constants.RECTDIST
        while y_pos < constants.HEIGHT:
            x_pos = constants.RECTDIST
            while x_pos < constants.WIDTH:
                pygame.draw.rect(self.screen, constants.GREY, (x_pos, y_pos, constants.RECTSIZE, constants.RECTSIZE))
                x_pos += constants.RECTSIZE + constants.RECTDIST
            y_pos += constants.RECTSIZE + constants.RECTDIST

    def draw_agents(self):
        agents = self.system.agents
        for name, agent in agents.items():
            color = agent.color
            pos = self.get_grid_pos(agent.x_pos, agent.y_pos)
            pygame.draw.rect(self.screen, color, (pos[0], pos[1], constants.RECTSIZE - 8, constants.RECTSIZE - 8))
            text = str(agent.agent_id)
            font = self.font
            text = font.render(text, True, constants.BLACK)
            self.screen.blit(text, (pos[0], pos[1]))


    @staticmethod
    def get_grid_pos(x, y):
        return int(x * (constants.RECTSIZE + constants.RECTDIST) + 5 * constants.RECTDIST), \
               int(y * (constants.RECTSIZE + constants.RECTDIST) + 5 * constants.RECTDIST)
