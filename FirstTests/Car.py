import random as rd
import numpy as np

class Car:
    def __init__(self,identity,position, battery = 100, rank = 0,speed = 25,direction = (1,0),neighbour_id = [], size = (4.5, 2, 1.5), vscore = 0, comRange = 10, role = "nothing", neighbourg_role = []):
        self.id = identity
        self.rank = rank
        self.battery = battery
        self.speed = speed
        self.pos = position
        self.dir = direction
        self.neighbour_id = neighbour_id
        self.size = size                    # size = (length, width, heigth)
        self.vscore = vscore
        self.comRange = comRange
        self.role = role
        self.neighbourg_role = neighbourg_role

def createListOfCar(numberOfCar, numberOfLane, lengthLane, double = "yes"):
    listCar = []
    for i in range(numberOfCar):
        if double == "yes":
            listCar.append(Car(i, (rd.uniform(-(lengthLane/2),lengthLane/2),rd.randint(-numberOfLane,numberOfLane-1)+0.5), rd.randint(0,100)))
        else:
            listCar.append(Car(i, (rd.uniform(-(lengthLane/2),lengthLane/2),rd.randint(0,numberOfLane-1)+0.5),rd.randint(0,100)))
    return listCar