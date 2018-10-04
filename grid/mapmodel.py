import math


class MapModel(object):

    def __init__(self):

        # what center is shown, -1 is no center
        self.center = -1
        self.centers = []
        self.cars = []
        self.clients = []

    def update(self):
        if self.center != -1:
            # only update if city is shown
            for car in self.cars[self.center]:
                if(car.pos[0] == car.dest[0] and
                   car.pos[1] == car.dest[1]):
                    if (car.dest[0] == car.dest2[0] and
                        car.dest[1] == car.dest2[1]):

                        for client in self.clients[self.center]:
                            if (client[2] == car.dest2[0] and
                                client[3] == car.dest2[1]):
                                self.clients[self.center].remove(client)
                                break
                        print("dropped client")
                        car.makeAvailable()
                    else:
                        for client in self.clients[self.center]:
                            if (client[0] == car.dest[0] and
                                client[1] == car.dest[1]):
                                client[4] = False
                                print("Client 4 set to false")
                                break
                        print("reached client")
                        car.dest = car.dest2
                    car.chooseMovement()

                car.update()

    def addCenter(self, centerData):
        print(centerData)
        print("adding: %s" % centerData[0])
        self.centers.append(centerData[0])
        self.clients.append([])
        list = []
        for idx in range(int(centerData[1])):
            list.append(Car(centerData[2], int(centerData[3])))
        self.cars.append(list)

    def addClient(self, clientData):
        print(clientData)
        for idx in range(len(self.centers)):
            if self.centers[idx] == clientData[0]:
                list = []
                for x in clientData[1:]:
                    list.append(int(x))
                list.append(True)
                self.clients[idx].append(list)
                break
        print(self.clients)



    def inACenter(self, click):
        for idx in range(len(self.centers)):
            if MapModel.inCircle(click, constants.CENTERPROPS[idx][1]):
                print("switching to center " + str(idx) )
                self.center = idx

    @staticmethod
    def inCircle(click, point):
        return ((math.pow((click[0] - point[0]), 2)) +
                math.pow((click[1] - point[1]), 2) <
                pow(constants.CENTERRADIUS, 2))
