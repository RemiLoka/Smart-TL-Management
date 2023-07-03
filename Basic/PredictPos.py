import numpy as np
import traci

def FuturPos(vehicle, dt = 1):
    angle = traci.vehicle.getAngle(vehicle)
    accel = traci.vehicle.getAcceleration(vehicle)
    speed = traci.vehicle.getSpeed(vehicle)
    pos = traci.vehicle.getPosition(vehicle)
    futurPos = [np.cos(angle)*((1/2)*accel*(dt**2) + speed*dt) + pos[0],np.sin(angle)*((1/2)*accel*(dt**2) + speed*dt) + pos[1]]
    return futurPos

def Direction(vehicle, posTL):
    dir = 'TL'
    angle = traci.vehicle.getAngle(vehicle)
    pos = traci.vehicle.getPosition(vehicle)
    dx = pos[0]-posTL[0]
    dy = pos[1]-posTL[1]
    if ((dx >= 0) and (dy >= 0)):
        if 0 <= angle <= 90:
            exit = "moves away"
            if angle <= 45:
                dir = 'north'
            else:
                dir = 'est'
        else:
            exit = "in approach"
    elif ((dx <= 0) and (dy >= 0)):
        if 90 <= angle <= 180:
            exit = "moves away"
            if angle <= 135:
                dir = 'est'
            else:
                dir = 'south'
        else:
            exit = "in approach"
    elif ((dx <= 0) and (dy <= 0)):
        if 180 <= angle <= 270:
            exit = "moves away"
            if angle <= 225:
                dir = 'south'
            else:
                dir = 'west'
        else:
            exit = "in approach"
    elif ((dx >= 0) and (dy <= 0)):
        if 270 <= angle <= 360:
            exit = "moves away"
            if angle <= 315:
                dir = 'west'
            else:
                dir = 'north'
        else:
            exit = "in approach"
    return exit +' to '+ dir + ' with ' + str(angle) + ' degree'