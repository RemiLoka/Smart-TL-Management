'''

@author: RemiLoka

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculationError(VehicleID, dt=1):
    '''
    This function modifies the memorybasics.csv file to add the errors and average errors for each VehicleID
    The error between the predicted position at time t + dt and the actual value
    
            Parameters:
                    VehicleID (string): the vehicle for which we wish to calculate the errors
                    dt (int): the step, by default: 1s
    '''
    df = pd.read_csv("memorybasics.csv")
    sumx = 0
    sumy = 0
    listIndex = list(np.where(df["Information"] == 'vehicle: %s'%VehicleID)[0])
    listTuple = tuple(listIndex)
    if dt == 1:
        pass
    else:
        for i in range(len(listTuple)):
            if i%dt == 0:
                pass
            else:
                listIndex.remove(listTuple[i])
    if listIndex == []:
        exit
    for i in range(1,len(listIndex)):
        errorX = np.abs(df.loc[listIndex[i-1]+2, 'x'] - df.loc[listIndex[i]+1, 'x'])
        sumx = sumx + errorX
        df.loc[listIndex[i], 'error x'] = errorX
        errorY = np.abs(df.loc[listIndex[i-1]+2, 'y'] - df.loc[listIndex[i]+1, 'y'])
        sumy = sumy + errorY
        df.loc[listIndex[i], 'error y'] = errorY
    if (len(listIndex)-1) == 0:
        df.loc[listIndex[0], 'means x'] = sumx
        df.loc[listIndex[0], 'means y'] = sumy
    else:
        df.loc[listIndex[0], 'means x'] = sumx/(len(listIndex)-1)
        df.loc[listIndex[0], 'means y'] = sumy/(len(listIndex)-1)
    df.to_csv('memorybasics.csv', index=False)

def calculationTot():
    '''
    This function modifies the memorybasics.csv file to add the total errors
    Needs to be used after the calculationError function
    '''
    df = pd.read_csv("memorybasics.csv")
    df['bool'] = pd.notna(df["means x"])
    listIndex = list(np.where(df["bool"] == True)[0])
    df.drop(df.columns[7], axis = 1, inplace = True)
    sum = 0
    for i in listIndex:
        sum = sum + df.loc[i, 'means x'] + df.loc[i, 'means y']
    means = sum/(2*len(listIndex))
    df.loc[0, 'tot'] = means
    df.to_csv('memorybasics.csv', index=False)
    return means

def traceCurve():
    df = pd.read_csv("/Users/remi/Desktop/ContenuStage/Smart-TL-Management/Basic/time.csv")
    listValue = []
    y_max = []
    y_min = []
    listTotLenVeh = df.loc[:,'Nb car']
    listTotLenVeh = list(set(listTotLenVeh))
    for number in listTotLenVeh:
        listIndex = []
        listIndex = list(np.where(df["Nb car"] == number))
        sum = 0
        listTime = []
        for index in listIndex[0]:
            sum = sum + df.loc[index, 'time']
            listTime.append(df.loc[index, 'time'])
        sum = sum/len(listIndex[0])
        listValue.append(sum)
        y_max.append(max(listTime))
        y_min.append(min(listTime))
    print(type(listTotLenVeh),type(listValue))
    plt.plot(listTotLenVeh, listValue,'r',listTotLenVeh,y_min,'g')
    plt.xlabel('number of vehicles')
    plt.ylabel('execution time')
    plt.legend(["average","min"])
    plt.show()

def graphCHpie(qty,lenListVeh):
    labels = 'CH','CHbck','CM'
    fig, ax = plt.subplots()
    ax.pie(qty, labels=labels, autopct='%1.1f%%')
    plt.title('distribution for %s vehicles' %str(lenListVeh))
    plt.show()

def curveCH():
    df = pd.read_csv("/Users/remi/Desktop/ContenuStage/Smart-TL-Management/Basic/CH.csv")
    listValueCH = []
    listValueCHbck = []
    listValueCM = []
    lenTot = df.loc[:,'lenVeh']
    lenTot = list(set(lenTot))
    for number in lenTot:
        listIndex = []
        listIndex = list(np.where(df["lenVeh"] == number))
        sumCH = 0
        sumCHbck = 0
        sumCM = 0
        for index in listIndex[0]:
            sumCH = sumCH + df.loc[index, 'CH']
            sumCHbck = sumCHbck + df.loc[index, 'CHbck']
            sumCM = sumCM + df.loc[index, 'CM']
        sumCH = sumCH/(len(listIndex[0])*number)
        listValueCH.append(sumCH)
        sumCHbck = sumCHbck/(len(listIndex[0])*number)
        listValueCHbck.append(sumCHbck)
        sumCM = sumCM/(len(listIndex[0])*number)
        listValueCM.append(sumCM)
    x = np.array(lenTot)
    y1 = np.array(listValueCH)
    y2 = np.array(listValueCHbck)
    y3 = np.array(listValueCM)
    
    # plot bars in stack manner
    plt.fill_between(x, y3+y2, y1+y2+y3, color = 'r')
    plt.fill_between(x, y3, y3 + y2, color = 'y')
    plt.fill_between(x, 0, y3, color = 'b')
    plt.xlabel("Number of vehicles")
    plt.ylabel("Percentage")
    plt.legend(["CH", "CHbck", "CM"])
    plt.title("Proportion of roles in the simulation")
    plt.show()

curveCH()