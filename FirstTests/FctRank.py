import numpy as np

def detectNeighbourg(listCar):
    numberOfCar = len(listCar)
    for i in range(numberOfCar):
        radius = listCar[i].comRange
        listCar[i].neighbour_id = []
        for j in range(numberOfCar):
            if i == j:
                pass
            else:   
                if ((np.sqrt((listCar[i].pos[0]-listCar[j].pos[0])**2+(listCar[i].pos[1]-listCar[j].pos[1])**2) <= radius) and (listCar[i].pos[1]*listCar[j].pos[1] > 0)):
                    listCar[i].neighbour_id.append(listCar[j].id)

def Mat(listCar, id):
    numberOfCar = len(listCar)
    idPos = None
    for i in range(numberOfCar):
        if id == listCar[i].id:
            idPos = i
    if idPos == None:
        print("Erreur") 
    listNb = listCar[idPos].neighbour_id
    nbNb = len(listNb)
    listPos = []
    listPos.append(idPos)
    for i in range(numberOfCar):
        if listCar[i].id in listNb:
            listPos.append(i)
    A = np.zeros((nbNb +1,nbNb +1))
    for i in range(nbNb +1):
        for j in range(nbNb +1):
            if listCar[listPos[i]].id in listCar[listPos[j]].neighbour_id:
                A[i,j] = 1
    return A

def EBM(listCar, id):
    M = Mat(listCar, id)
    A2 = np.linalg.matrix_power(M, 2)
    B = 0
    for i in range(len(M)):
        for j in range(len(M)):
            if i<j and M[i,j] == 0:
                B += 1/(A2[i,j])
    listCar[id].vscore = B*listCar[id].battery
    return B*listCar[id].battery

def roleCar(listCar):
    numberOfCar = len(listCar)
    for j in range(len(listCar)):
        listNb = listCar[j].neighbour_id
        nbNb = len(listNb)
        if nbNb == []:
            listCar[j].role = "CH"
        listPos = []
        listVscore =[]
        listPos.append(listCar[j].id)
        listVscore.append(listCar[j].vscore)
        for i in range(numberOfCar):
            if listCar[i].id in listNb:
                listPos.append(i)
                listVscore.append(listCar[i].vscore)
        posCHbck = 0
        for i in range(nbNb +1):
            if i == 0:
                vscore = listVscore[i]
                posCH = i
            else:
                if listVscore[i] >= vscore:
                    vscore = listVscore[i]
                    posCHbck = posCH
                    posCH = i
        for i in range(nbNb+1):
            if i == posCH:
                listCar[listPos[i]].role = "CH"
            elif i == posCHbck:
                listCar[listPos[i]].role = "CHbck"
            if i != posCH and i != posCHbck:
                listCar[listPos[i]].role = "CM"
    listCM = []
    for j in range(len(listCar)):
        if listCar[j].role == "CM":
            listCM.append(j)
    for j in range(len(listCM)):
        neighbour_role = []
        neighbour_score = []
        for i in range(len(listCar[listCM[j]].neighbour_id)):
            neighbour_role.append(listCar[listCar[listCM[j]].neighbour_id[i]].role)
            neighbour_score.append(listCar[listCar[listCM[j]].neighbour_id[i]].vscore)
        if "CH" in neighbour_role:
            pass
        else:
            maximum_val= neighbour_score[0]
            for n in range(1, len(neighbour_score)): 
                if (neighbour_score[n] > maximum_val):
                    maximum_val = neighbour_score[n]
            listCar[listCar[listCM[j]].neighbour_id[neighbour_score.index(maximum_val)]].role = "CH"
    listCH = []
    for j in range(len(listCar)):
        if listCar[j].role == "CH":
            listCH.append(j)
    for j in range(len(listCH)):
        neighbour_role = []
        neighbour_score = []
        if len(listCar[listCH[j]].neighbour_id) == 0:
            pass
        else:
            for i in range(len(listCar[listCH[j]].neighbour_id)):
                neighbour_role.append(listCar[listCar[listCH[j]].neighbour_id[i]].role)
                neighbour_score.append(listCar[listCar[listCH[j]].neighbour_id[i]].vscore)
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
                listCar[listCar[listCH[j]].neighbour_id[neighbour_score.index(maximum_val)]].role = "CHbck"