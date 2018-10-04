import pygame


class GridControl(object):

    def __init__(self, model):
        self.model = model

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
