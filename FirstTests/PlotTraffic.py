import matplotlib.pyplot as plt

def plotTraffic(listCar,numberLane,sizeLane,time):
    posCarX = []
    posCarY = []
    posCarXCH = []
    posCarYCH = []
    posCarXCHbck = []
    posCarYCHbck = []
    posCarXCM = []
    posCarYCM = []
    roleCar = []
    nbCH = 0
    nbCHbck = 0
    nbCM = 0

    for i in range(len(listCar)):
        posCarX.append(listCar[i].pos[0])
        posCarY.append(listCar[i].pos[1])
        roleCar.append(listCar[i].role)
        if listCar[i].role == "CH":
            posCarXCH.append(listCar[i].pos[0])
            posCarYCH.append(listCar[i].pos[1]) 
            nbCH = nbCH + 1
        elif listCar[i].role == "CHbck":
            posCarXCHbck.append(listCar[i].pos[0])
            posCarYCHbck.append(listCar[i].pos[1])
            nbCHbck = nbCHbck + 1       
        elif listCar[i].role == "CM":
            posCarXCM.append(listCar[i].pos[0])
            posCarYCM.append(listCar[i].pos[1])
            nbCM = nbCM + 1

    fig, ax = plt.subplots()
    plt.plot(posCarXCH,posCarYCH,"or")
    plt.plot(posCarXCHbck,posCarYCHbck,"oy")
    plt.plot(posCarXCM,posCarYCM,"ob")
    for i in range(len(listCar)):
        #  plt.text(posCarX[i] - 0.2,posCarY[i] + 0.1,f"Id: {i}",fontsize=11)
        #  plt.text(posCarX[i] - 0.2,posCarY[i] - 0.2,f"{round(EBM(listCar,i),2)}",fontsize=11)
        if listCar[i].role == "CH":
            ax.add_patch(plt.Circle((posCarX[i],posCarY[i]), listCar[i].comRange, color='r',fill=False))
    for i in range(-numberLane,numberLane+1):
        if i == 0 or i == -numberLane or i == numberLane:
            plt.axhline(i,color='black')
        else:
            plt.axhline(i,color='gray',linestyle='--')
    ax.set_aspect('equal', adjustable='datalim')
    ax.text(-sizeLane/2, sizeLane/2 - sizeLane/4,f"Number of cars: {len(listCar)}\nCH: {nbCH} // CHbck: {nbCHbck} // CM: {nbCM}\n1st-time execution: {round(1000*(time),2)} ms",fontsize=11, style='italic', bbox={'facecolor': 'lightblue', 'alpha': 0.5, 'pad': 10})
    plt.show()

