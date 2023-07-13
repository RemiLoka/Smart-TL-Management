import numpy as np
import traci
from copy import copy

def detectNeighbourg(listID, comRange = 50):
    '''
    This function returns all neighbours within the given radius (comRange)

            Parameters:
                    listID (list or tuple): a list of vehicle
                    comRange (int): Radius, default set at 50m

            Returns:
                    neighbour_id (list): list of neighbour IDs
                    neighbour_place (list): list with the index lists of the listID's neighbours
    '''
    neighbour_id = []
    neighbour_place = [] 
    listPos = []
    numberOfCar = len(listID)
    for vehicle in listID:
        listPos.append(traci.vehicle.getPosition(vehicle))
    for i in range(numberOfCar):
        neighbour_idi = []
        neighbour_placei = []
        for j in range(numberOfCar):
            if i == j:
                pass
            elif((np.sqrt((listPos[i][0]-listPos[j][0])**2+(listPos[i][1]-listPos[j][1])**2) <= comRange) and (traci.vehicle.getAngle(listID[j]) - 45 < traci.vehicle.getAngle(listID[i]) < traci.vehicle.getAngle(listID[j]) + 45)):
                neighbour_idi.append(listID[j])
                neighbour_placei.append(j)
        neighbour_id.append(neighbour_idi)
        neighbour_place.append(neighbour_placei)
    [str(x) for x in neighbour_id]
    return neighbour_id, neighbour_place

def roleCar(listID, listNeighbor):
    '''
    This function returns the roles of vehicle: Cluster Head (CH), Cluster Head Backup (CHbck) and Cluster Master (CM)

            Parameters:
                    listID (list or tuple): a list of vehicle
                    listNeighbor (tuple): return of detectNeighbourg(listID)

            Returns:
                    listRole (list): list of roles
                    listID (list): list of vehicles with a fixed role
    '''
    listNeighbor
    numberOfCar = len(listID)
    listRank = []

    for i in range(numberOfCar):                # Creation Matrix
        listNb = listNeighbor[0][i].copy()
        listNb.insert(0,listID[i])
        listIndex = listNeighbor[1][i].copy()
        listIndex.insert(0,i)
        nbNb = len(listNb)
        A = np.zeros((nbNb,nbNb))
        for n in range(nbNb):
            for m in range(nbNb):
                if n == m:
                    A[n,m] = 0
                elif listID[listIndex[n]] in listNeighbor[0][listIndex[m]]:
                    A[n,m] = 1

        A2 = np.linalg.matrix_power(A, 2)       # Calcul EBM score
        B = 0
        for i in range(len(A)):
            for j in range(len(A)):
                if i<j and A[i,j] == 0:
                    B += 1/(A2[i,j])
        listRank.append(B)

    listRole = [0]*numberOfCar                  # Assignement role
    listCM = []
    for j in range(numberOfCar):
        listNb = listNeighbor[0][j].copy()
        listPos = listNeighbor[1][j].copy()
        nbNb = len(listNb)
        if listNeighbor[0][j] == []:
            listRole[j] = "CH"
        listRankNb =[]
        listPos.insert(0,j)
        listRankNb.append(listRank[j])
        for i in listPos:
            listRankNb.append(listRank[i])
        posCHbck = 0
        for i in range(nbNb +1):
            if i == 0:
                vscore = listRankNb[i]
                posCH = i
            else:
                if listRankNb[i] >= vscore:
                    vscore = listRankNb[i]
                    posCHbck = posCH
                    posCH = i
        for i in range(nbNb+1):
            if i == posCH:
                listRole[listPos[i]] = "CH"
            elif i == posCHbck:
                listRole[listPos[i]] = "CHbck"
            if i != posCH and i != posCHbck:
                listRole[listPos[i]] = "CM"
                listCM.append(listPos[i])

    for j in listCM:                            # Verification CM
        neighbour_role = []
        neighbour_score = []
        for pos in listNeighbor[1][j]:
            neighbour_role.append(listRole[pos])
            neighbour_score.append(listRank[pos])
        if "CH" in neighbour_role:
            pass
        else:
            maximum_val= neighbour_score[0]
            for n in range(1, len(neighbour_score)): 
                if (neighbour_score[n] > maximum_val):
                    maximum_val = neighbour_score[n]
            listRole[listNeighbor[1][j][neighbour_score.index(maximum_val)]] = "CH"

    listCH = []                                 # Verification CHbck
    for j in range(numberOfCar):
        if listRole[j] == "CH":
            listCH.append(j)
    for j in listCH:
        neighbour_role = []
        neighbour_score = []
        if listNeighbor[0][j] == []:
            pass
        else:
            for pos in listNeighbor[1][j]:
                neighbour_role.append(listRole[pos])
                neighbour_score.append(listRank[pos])
            if "CHbck" in neighbour_role:
                pass
            else:
                maximum_val= neighbour_score[0]
                for n in range(1, len(neighbour_score)): 
                    if neighbour_role[n] == "CH":
                        pass
                    else:
                        if (neighbour_score[n] > maximum_val):
                            maximum_val = neighbour_score[n]
                listRole[listNeighbor[1][j][neighbour_score.index(maximum_val)]] = "CHbck"
    return listRole, listID

def maintainCH(listID, listIDassigned, listRole, listNeighbor ):
    for i in range(len(listID)):
        listNbi = listNeighbor[i]
        if listID in listIDassigned:
            pass
            for j in range(len(listNeighbor)):
                if listNeighbor[j] in listIDassigned:
                    pass
                else:
                    NotAssigned = 1
        else:
            NotAssigned = 1
        if NotAssigned == 1:
            roleCar(listNbi + listID[i], listNeighbor)
            

def assignColor(listID, listRole):
    '''
    This function assigns colours to vehicles according to their roles : CH: red, CHbck: greed, CM: blue
    If there is a mistake when assigning roles, the car will be white. By default, sumo cars are yellow.
    
            Parameters:
                    listRole (list): list of roles
                    listID (list): list of vehicles with a fixed role

            Returns:
                    nbCH (int): number of Cluster Head
                    nbCHbck (int): number of Cluster Head Backup
                    nbCM (int): number of Cluster Master
    '''
    nbCH = 0
    nbCHbck = 0
    nbCM = 0
    for i in range(len(listID)):
        if listRole[i] == "CH":
            traci.vehicle.setColor(listID[i],[255,0,0,255])     # red
            nbCH = nbCH + 1
        elif listRole[i] == "CHbck":
            traci.vehicle.setColor(listID[i],[0,255,0,255])     # green
            nbCHbck = nbCHbck + 1
        elif listRole[i] == "CM":
            traci.vehicle.setColor(listID[i],[0,0,255,255])     # blue
            nbCM = nbCM +1
        else:
            traci.vehicle.setColor(listID[i],[255,255,255,255]) # white
    return nbCH, nbCHbck, nbCM