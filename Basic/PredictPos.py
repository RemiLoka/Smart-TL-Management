import numpy as np
import traci

def EuclideanDistance(a,b):
    '''
    Returns the euclidean distance of two position (x,y).

            Parameters:
                    a (tuple of float): postion (x,y)
                    b (tuple of float): postion (x,y)

            Returns:
                    Euclidean Distance (str): distance
    '''
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def FuturPos(vehicle, dt = 1):
    '''
    This function predict the futur position of a vehicle to time dt

            Parameters:
                    vehicle (string): Id of the vehicle
                    dt (int): step time: by default set to 1s 

            Returns:
                    futurPos (tuple): postion (x,y)
    '''
    angle = traci.vehicle.getAngle(vehicle)
    accel = traci.vehicle.getAcceleration(vehicle)
    speed = traci.vehicle.getSpeed(vehicle)
    pos = traci.vehicle.getPosition(vehicle)
    futurPos = [np.cos(angle)*((1/2)*accel*(dt**2) + speed*dt) + pos[0],np.sin(angle)*((1/2)*accel*(dt**2) + speed*dt) + pos[1]]
    return futurPos

def Direction1pos(vehicle, posTL):
    '''
    This function returns if a vehicle is in approach of a traffic lighter or if the vehicle move away.

            Parameters:
                    vehicle (string): Id of the vehicle
                    postTL (tuple): postion of the traffic lighter

            Returns:
                    prev (str): 'moves away' or 'in approach'
                    dir (str): where the vehicle is heading
    '''
    dir = 'TL'
    angle = traci.vehicle.getAngle(vehicle)
    pos = traci.vehicle.getPosition(vehicle)
    dx = pos[0]-posTL[0]
    dy = pos[1]-posTL[1]
    if ((dx >= 0) and (dy >= 0)):
        if 0 <= angle <= 90:
            prev = "moves away"
            if angle <= 45:
                dir = 'north'
            else:
                dir = 'est'
        else:
            prev = "in approach"
    elif ((dx <= 0) and (dy >= 0)):
        if 90 <= angle <= 180:
            prev = "moves away"
            if angle <= 135:
                dir = 'est'
            else:
                dir = 'south'
        else:
            prev = "in approach"
    elif ((dx <= 0) and (dy <= 0)):
        if 180 <= angle <= 270:
            prev = "moves away"
            if angle <= 225:
                dir = 'south'
            else:
                dir = 'west'
        else:
            prev = "in approach"
    elif ((dx >= 0) and (dy <= 0)):
        if 270 <= angle <= 360:
            prev = "moves away"
            if angle <= 315:
                dir = 'west'
            else:
                dir = 'north'
        else:
            prev = "in approach"
    return prev, dir

def InformedCar(vehicle, listPosTL):
    '''
    This function returns for a vehicle the traffic lighter from which it leaves and the one it is supposed to arrive at.

            Parameters:
                    vehicle (string): Id of the vehicle
                    listPostTL (list): list of postions of the traffic lighters

            Returns:
                    minApproach (tuple): position of the next traffic lighter
                    minAway (tuple): position of the previous traffic lighter
                    prev[1] : global direction (north, est, west, south or TL if no previous traffic lighters)
    '''
    pos = traci.vehicle.getPosition(vehicle)
    if len(listPosTL) == 0:
        return 'need TL pos'
    elif len(listPosTL) == 1:
        prev = Direction1pos(vehicle,listPosTL)
        return prev
    else:
        nbTL = len(listPosTL)
        disTL = []
        listApproach = []
        disTLApproach = []
        listAway = []
        disTLAway = []
        minApproach = 0
        minAway = 0
        for i in range(nbTL):
            prev = Direction1pos(vehicle,listPosTL[i])
            disTL.append(EuclideanDistance(pos,listPosTL[i]))
            if prev[0] == "in approach":
                listApproach.append(listPosTL[i])
                disTLApproach.append(EuclideanDistance(pos,listPosTL[i]))
                if minApproach == 0:
                    minApproach = listPosTL[i]
                    minIndexApp = i
                else:
                    if EuclideanDistance(pos,listPosTL[i]) < disTL[minIndexApp]:
                        minApproach = listPosTL[i]
            elif prev[0] == "moves away":
                listAway.append(listPosTL[i])
                disTLAway.append(EuclideanDistance(pos,listPosTL[i]))
                if minAway == 0:
                    minAway = listPosTL[i]
                    minIndexAway = i
                else:
                    if EuclideanDistance(pos,listPosTL[i]) < disTL[minIndexAway]:
                        minAway = listPosTL[i]
        return minApproach, minAway, prev[1]