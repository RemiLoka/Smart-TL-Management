import numpy as np
import traci

def FuturPos(vehicle, dt = 1):
    angle = traci.vehicle.getAngle(vehicle)
    accel = traci.vehicle.getAcceleration(vehicle)
    speed = traci.vehicle.getSpeed(vehicle)
    pos = traci.vehicle.getPosition(vehicle)
    futurPos = [np.cos(angle)*((1/2)*accel*(dt**2) + speed*dt) + pos[0],np.sin(angle)*((1/2)*accel*(dt**2) + speed*dt) + pos[1]]
    return futurPos