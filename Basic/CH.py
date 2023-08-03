'''

@author: RemiLoka

'''

import numpy as np
import traci
from copy import copy

def detectNeighbourg(listID, comRange = 100):
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

def roleCar(listID, listNeighbor, initialisation = 'yes', notAssignedIndex = [], listRole = [], listRank = []):
    '''
    This function returns the roles of vehicle: Cluster Head (CH), Cluster Head Backup (CHbck) and Cluster Master (CM)

            Parameters:
                    listID (list or tuple): a list of vehicle
                    listNeighbor (tuple): return of detectNeighbourg(listID)

            Optionnal Parameters:
                    initialisation (str): default value is 'yes', if it is a maintenance, change its value
                    notAssignedIndex (list): return of removeOldCar function
                    listRole (list): list of roles from the previous calculation
                    listRank(list): list of score from the previous calculation

            Returns:
                    listRole (list): list of roles
                    listID (list): list of vehicles with a fixed role
                    listRank (list): list of score
    '''
    
    numberOfCar = len(listID)

########## For init ##########

    if initialisation == 'yes':
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
            for n in range(len(A)):
                for m in range(len(A)):
                    if n<m and A[n,m] == 0:
                        B += 1/(A2[n,m])
            listRank.append(B)

        listRole = [0]*numberOfCar                  # Assignement role
        for i in range(numberOfCar):
            listNb = listNeighbor[0][i].copy()
            listPos = listNeighbor[1][i].copy()
            nbNb = len(listNb)
            if nbNb == 0:                               # no neighbours
                listRole[i] = "CH"
            elif nbNb == 1:                             # a single neighbour
                if (listRole[i] != 0) and (listRole[listPos[0]] != 0):
                    if (listRole[i] == 'CH') or (listRole[listPos[0]] == 'CH'):
                        pass
                    else:
                        listRole[i] == 'CHbck'
                        listRole[listPos[0]] == 'CH'
                elif (listRole[i] == 0) and (listRole[listPos[0]] != 0):
                    if listRole[listPos[0]] == 'CH':
                        listRole[i] = 'CHbck'
                    else:
                        listRole[listPos[0]] = 'CHbck'
                        listRole[i] = 'CH'
                elif (listRole[i] != 0) and (listRole[listPos[0]] == 0):
                    if listRole[i] == 'CH':
                        listRole[listPos[0]] = 'CHbck'
                    else:
                        listRole[i] = 'CHbck'
                        listRole[listPos[0]] = 'CH'
                else:
                        listRole[i] = 'CHbck'
                        listRole[listPos[0]] = 'CH'
            else:                                       # more than one neighbour
                withoutRole = []
                listCMNb = []
                ch = 0
                chbck = 0
                listPos.insert(0,i)
                for j in listPos:
                    if listRole[j] == 'CH':
                        ch = ch + 1
                    elif listRole[j] == 'CHbck':
                        chbck = chbck + 1
                    elif listRole[j] == 0:
                        withoutRole.append(j)
                    elif listRole[j] == 'CM':
                        listCMNb.append(j)
                for j in withoutRole:
                    listRole[j] = 'CM'
                if ch >= 1 and chbck >= 1:
                    for k in withoutRole+listCMNb:
                        listRole[k] = 'CM'
                elif ch >= 1 and chbck == 0:
                    max = 0
                    maxindex = 'no'
                    for k in withoutRole+listCMNb:
                        if listRank[k] >= max:
                            max = listRank[k]
                            maxindex = k
                    if maxindex != 'no':
                        listRole[maxindex] = 'CHbck'
                    else:
                        listRole[withoutRole[-1]] = 'CHbck'
                elif ch == 0 and chbck >= 1:
                    max = 0
                    maxindex = 'no'
                    for k in withoutRole+listCMNb:
                        if listRank[k] >= max:
                            max = listRank[k]
                            maxindex = k
                    listRole[maxindex] = 'CH'
                else:
                    max = 0
                    maxindex = 'no'
                    secondindex = 'no'
                    for k in withoutRole+listCMNb:
                        if listRank[k] >= max:
                            max = listRank[k]
                            secondindex = maxindex
                            maxindex = k
                    if maxindex != 'no' and secondindex != 'no':
                        listRole[maxindex] = 'CH'
                        listRole[secondindex] = 'CHbck'
                    elif maxindex != 'no':
                        listRole[maxindex] = 'CH'
                        if withoutRole[-1] != maxindex:
                            listRole[withoutRole[-1]] = 'CHbck'
                        else:
                            listRole[withoutRole[0]] = 'CHbck'

########## In the case of maintenance ##########

    else:
        for i in notAssignedIndex:                # Creation Matrix
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
            for n in range(len(A)):
                for m in range(len(A)):
                    if n<m and A[n,m] == 0:
                        B += 1/(A2[n,m])
            listRank[i] = B
                  
        for i in notAssignedIndex:      # Assignement role
            listNb = listNeighbor[0][i].copy()
            listPos = listNeighbor[1][i].copy()
            nbNb = len(listNb)
            if nbNb == 0:                               # no neighbours
                listRole[i] = "CH"
            elif nbNb == 1:                             # a single neighbour
                if(listRole[listPos[0]] != 0):
                    if listRole[listPos[0]] == 'CH':
                        listRole[i] = 'CHbck'
                    else:
                        listRole[listPos[0]] = 'CHbck'
                        listRole[i] = 'CH'
                else:
                        listRole[i] = 'CHbck'
                        listRole[listPos[0]] = 'CH'
            else:                                       # more than one neighbour
                withoutRole = []
                listCMNb = []
                ch = 0
                chbck = 0
                listPos.insert(0,i)
                for j in listPos:
                    if listRole[j] == 'CH':
                        ch = ch + 1
                    elif listRole[j] == 'CHbck':
                        chbck = chbck + 1
                    elif listRole[j] == 0:
                        withoutRole.append(j)
                    elif listRole[j] == 'CM':
                        listCMNb.append(j)
                for j in withoutRole:
                    listRole[j] = 'CM'
                if ch >= 1 and chbck >= 1:
                    pass
                elif ch >= 1 and chbck == 0:
                    max = 0
                    maxindex = 'no'
                    for k in withoutRole+listCMNb:
                        if listRank[k] >= max:
                            max = listRank[k]
                            maxindex = k
                    if maxindex != 'no':
                        listRole[maxindex] = 'CHbck'
                    else:
                        listRole[withoutRole[-1]] = 'CHbck'
                elif ch == 0 and chbck >= 1:
                    max = 0
                    maxindex = 'no'
                    for k in withoutRole+listCMNb:
                        if listRank[k] >= max:
                            max = listRank[k]
                            maxindex = k
                    listRole[maxindex] = 'CH'
                else:
                    max = 0
                    maxindex = 'no'
                    secondindex = 'no'
                    for k in withoutRole+listCMNb:
                        if listRank[k] >= max:
                            max = listRank[k]
                            secondindex = maxindex
                            maxindex = k
                    if maxindex != 'no' and secondindex != 'no':
                        listRole[maxindex] = 'CH'
                        listRole[secondindex] = 'CHbck'
                    elif maxindex != 'no':
                        listRole[maxindex] = 'CH'
                        if withoutRole[-1] != maxindex:
                            listRole[withoutRole[-1]] = 'CHbck'
                        else:
                            listRole[withoutRole[0]] = 'CHbck'
    return listRole, listID, listRank

def removeOldCar(listID, listIDassigned, listRank, listRole):
    '''
    This function is used to prepare lists for maintenance of CH
            Parameters:
                    listID (list or tuple): a list of vehicle
                    listIDassigned (tuple): list of vehicle having already been assigned
                    listRank (list): list of EBM ranks
                    listRole (list): list of roles

            Returns:
                    notAssignedIndex (list): index in link with listID
    '''
    notAssignedIndex = []
    sup = -1
    add = -1
    for i in range(len(listIDassigned)):
        if listIDassigned[i] not in listID:
            sup = sup + 1
            del listRank[i - sup]
            del listRole[i - sup]
    for i in range(len(listID)):
        if listID[i] not in listIDassigned:
            add = add + 1
            listRank.insert(i,'no')
            listRole.insert(i,0)
            notAssignedIndex.append(i)
    return notAssignedIndex

def speedNeighbor(listIDassigned, listNeighbor,listRole):
    '''
    
    '''
    listAverageSpeed = []
    for i in range(len(listIDassigned)):
        listIDnb = listNeighbor[0][i].copy()
        listIDnb.insert(0,listIDassigned[i])
        listPos = listNeighbor[1][i].copy()
        listPos.insert(0,i)
        n = len(listPos)
        speedCH = 0
        sumSpeed = 0
        posCH = 'no'
        posCHbck = 'no'
        for j in range(n):
            if listRole[listPos[j]] == 'CH':
                speedCH = traci.vehicle.getSpeed(listIDnb[j])
                posCH = listPos[j]
            elif listRole[listPos[j]] == 'CHbck':
                posCHbck = listPos[j]
            sumSpeed = sumSpeed + traci.vehicle.getSpeed(listIDnb[j])
            
        if abs(sumSpeed - speedCH) > 8.34:          # 8.34
            if posCHbck == 'no' or posCH == 'no':
                pass
            else:
                listRole[posCH] = 'CHbck'
                listRole[posCHbck] = 'CH'
        listAverageSpeed.append(sumSpeed/n)
    return listAverageSpeed

def maintainCH(listID, listIDassigned, listRank, listRole, listNeighbor):
    '''
    
    '''
    notAssignedIndex = removeOldCar(listID,listIDassigned,listRank,listRole)
    [newListRole, listIDassigned, newListRank] = roleCar(listID, listNeighbor, 'no', notAssignedIndex, listRole, listRank)
    speedNeighbor(listID,listNeighbor,newListRole)
    return newListRole, listIDassigned, newListRank
        
def printRoleRankNeigbour(listID, listNeighbor,listRole, listRank):
    '''
    This function helps you to see the output of cH selection algorithms

            Parameters: 
                    listID (list or tuple): a list of vehicle
                    listNeighbor (tuple): list of vehicle having already been assigned
                    listRole (list): list of roles
                    listRank (list): list of EBM ranks
    '''
    for i in range(len(listID)):
        listRoleNb = []
        listRankNb = []
        listRoleNb.append(listRole[i])
        listRankNb.append(listRank[i])
        for j in listNeighbor[1][i]:
            listRoleNb.append(listRole[j])
            listRankNb.append(listRank[j])
        print(listRoleNb)
        print(listRankNb)

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
            traci.vehicle.setColor(listID[i],[255,0,0,255])
            nbCH = nbCH + 1
        elif listRole[i] == "CHbck":
            traci.vehicle.setColor(listID[i],[0,255,0,255])
            nbCHbck = nbCHbck + 1
        elif listRole[i] == "CM":
            traci.vehicle.setColor(listID[i],[0,0,255,255])
            nbCM = nbCM +1
        else:
            traci.vehicle.setColor(listID[i],[255,255,255,255])
    return nbCH, nbCHbck, nbCM