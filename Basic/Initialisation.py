'''@author: RemiLoka'''

import traci

def FindTL(net):
    '''
    This function extracts the position of red lights from the net file

            Parameters:
                    net: net file

            Returns:
                    traffic_pos: list of position of traffic lights
    '''
    node_ids = [node.getID() for node in net.getNodes()]
    traffic_pos = []

    for node in node_ids:
        if (net.getNode(node).getType()) == 'traffic_light':
            traffic_pos.append(net.getNode(node).getCoord())
    return traffic_pos

def ImportantLanes():
    '''
    This function extracts important lines and edges according to certain parameters

            Returns:
                    TotalBigEdge: list of important edges
                    TotalListLane: list of important lanes
                    TotalEdge: Edge before selection
                    TotalLane: Lanes before selection
    '''
    TotalLane = traci.lane.getIDList()
    TotalListLane = list(TotalLane)

    TotalEdge = traci.edge.getIDList()
    TotalBigEdge = list(TotalEdge)

    for edge in TotalEdge:
        if(traci.edge.getLaneNumber(edge) < 2):
            TotalBigEdge.remove(edge)

    for edge in TotalBigEdge:
        for lane in TotalLane:
            if(lane[0:10] in edge):
                if lane in TotalListLane:
                    TotalListLane.remove(lane)

    TotalLane = tuple(TotalListLane)

    TotalLane = tuple(TotalListLane)
    for lane in TotalLane:
        if(traci.lane.getMaxSpeed(lane)< 8.3):   #8.34 = 30 km/h
            TotalListLane.remove(lane)
    return TotalBigEdge, TotalListLane, TotalEdge, TotalLane

def ListVehicles(TotalBigEdge, TotalListLane):
    '''
    This function extracts the position of red lights from the net file

            Parameters:
                    TotalBigEdge: list of important edges
                    TotalListLane: list of important lanes

            Returns:
                    listVehID: list of vehicles present on the important edges and lanes
                    lenListVeh: len of listVehID
    '''
    listVehID = []

    for edge in TotalBigEdge:
        listVeh = traci.edge.getLastStepVehicleIDs(edge)
        listVehID = listVehID + list(listVeh)
    for lane in TotalListLane:
        listVeh = traci.lane.getLastStepVehicleIDs(lane)
        listVehID = listVehID + list(listVeh)
    
    listVehID.sort()
    listVehID = list(set(listVehID))

    lenListVeh = len(listVehID)
    return listVehID, lenListVeh