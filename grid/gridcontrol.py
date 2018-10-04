import pygame


class GridControl(object):

    def __init__(self, model):
        self.model = model

    @staticmethod
    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
