########## Import ##########

import time
import FirstTests.PlotTraffic as PlotTraffic
import FirstTests.Car as Car
import FirstTests.FctRank as FctRank

########## Defined Traffic ##########

numberCar = 100
numberLane = 3
sizeLane = 100
twoDirection = "yes"        #"yes" if you want two direction

listCar = Car.createListOfCar(numberCar,numberLane,sizeLane,twoDirection)

########## Creation Cluster + Initialisation CH ##########

timestart = time.time()

FctRank.detectNeighbourg(listCar)
for i in range(len(listCar)):
    FctRank.EBM(listCar,i)
FctRank.roleCar(listCar)

timeend = time.time()

########## Plot Road ##########

PlotTraffic.plotTraffic(listCar,numberLane,sizeLane,timeend-timestart)