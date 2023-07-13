import pandas as pd
import numpy as np

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