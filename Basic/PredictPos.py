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
    angle = traci.vehicle.getAngle(vehicle)
    pos = traci.vehicle.getPosition(vehicle)
    d = np.sqrt((posTL[0]-pos[0])**2+(posTL[1]-pos[1])**2)
    teta = np.arccos((posTL[0]-pos[0])/d)
    if posTL[1] > pos[1]:
        teta = (teta*180)/np.pi
    else:
        teta = 360 - (teta*180)/np.pi
    if np.abs(teta - angle)< 90:
        return "en approche"
    else:
        return "s'éloigne"