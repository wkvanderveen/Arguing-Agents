import pygame

class GridControl(object):

    def __init__(self, model):
        self.model = model


    def serverEvent(self, data):
        stringData = data.decode("utf-8")
        id = stringData.split("=")
        # new center
        if id[0] == "center":
            self.model.addCenter(id[1].split(", "))
        # new client
        if id[0] == "client":
            self.model.addClient(id[1].split(","))

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
                self.model.inACenter(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.model.center = -1

        return False
