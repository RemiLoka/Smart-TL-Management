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
            for i in range(len(A)):
                for j in range(len(A)):
                    if i<j and A[i,j] == 0:
                        B += 1/(A2[i,j])
            listRank[i] = B

        listCM = []                                 # Assignement role
        for j in notAssignedIndex:
            listNb = listNeighbor[0][j].copy()
            listPos = listNeighbor[1][j].copy()
            nbNb = len(listNb)
            if listNeighbor[0][j] == []:
                listRole[j] = "CH"
            else:
                listRankNb = []
                ch = 0
                chbck = 0
                listPos.insert(0,j)
                listRankNb.append(listRank[j])
                for i in range(len(listPos)):
                    listRankNb.append(listRank[i])
                    if listRole[listPos[i]] == 'CH':
                        ch = 1
                        indexch = i
                    elif listRole[listPos[i]] == 'CHbck':
                        chbck = 1
                        indexchbck = i
                if (ch == 1 and chbck == 1):
                    listRole[i]='CM'

                elif (ch == 0 and chbck == 1 and len(listNeighbor[0][j]) == 1):
                    listRole[indexchbck] = 'CH'

                elif (ch == 0 and chbck == 1 and len(listNeighbor[0][j]) > 2):
                    listRole[indexchbck] = 'CH'
                    neighbour_role = []
                    neighbour_score = []
                    for pos in listPos:
                        neighbour_role.append(listRole[pos])
                        neighbour_score.append(listRank[pos])
                        maximum_val = neighbour_score[0]
                        for n in range(1, len(neighbour_score)): 
                            if (neighbour_score[n] > maximum_val) and (pos != indexchbck):
                                maximum_val = neighbour_score[n]
                    listRole[listPos[neighbour_score.index(maximum_val)]] = "CHbck"

                elif (ch == 1 and chbck == 0 and len(listNeighbor[0][j]) > 2):
                    neighbour_role = []
                    neighbour_score = []
                    for pos in listPos:
                        neighbour_role.append(listRole[pos])
                        neighbour_score.append(listRank[pos])
                        maximum_val = neighbour_score[0]
                        for n in range(1, len(neighbour_score)): 
                            if (neighbour_score[n] > maximum_val) and (pos != indexch):
                                maximum_val = neighbour_score[n]
                    listRole[listPos[neighbour_score.index(maximum_val)]] = "CHbck"
                
                else:
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
            print('del',i)
    for i in range(len(listID)):
        if listID[i] not in listIDassigned:
            add = add + 1
            listRank.insert(i,0 + add)
            listRole.insert(i,0 + add)
            print('append',i)
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
        posCHbck = 'no'
        for j in range(n):
            if listRole[listPos[j]] == 'CH':
                print(listIDnb[j])
                speedCH = traci.vehicle.getSpeed(listIDnb[j])
                posCH = listPos[j]
            elif listRole[listPos[j]] == 'CHbck':
                posCHbck = listPos[j]
            sumSpeed = sumSpeed + traci.vehicle.getSpeed(listIDnb[j])
            
        if abs(sumSpeed - speedCH) > 8.34:          # 8.34
            if posCHbck == 'no':
                pass
            else:
                listRole[posCH] = 'CHbck'
                listRole[posCHbck] = 'CH'
        listAverageSpeed.append(sumSpeed/n)
    return listAverageSpeed

def maintainCH(listID, listIDassigned, listRank, listRole, listNeighbor):
    '''
    
    '''
    listTEST = listID.copy()
    print('bf:','role',len(listRole),'rank',len(listRank),'id',len(listTEST),'\n')
    notAssignedIndex = removeOldCar(listID,listIDassigned,listRank,listRole)
    print('af:','role',len(listRole),'rank',len(listRank),'id',len(listTEST),'\n')
    [newListRole, listIDassigned, newListRank] = roleCar(listID, listNeighbor, 'no', notAssignedIndex, listRole, listRank)

#    speedNeighbor(listID,listNeighbor,newListRole)
    return newListRole, listIDassigned, newListRank
        

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