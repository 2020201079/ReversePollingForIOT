needDataFromSensor = {} # a dic with sensorid -> bool
dataReady = {} # a dic with sensorid -> bool
sensorData = {} # a dic with sensorid -> data

def fetchData(sensorID):
    return "Fetch data is called with sensor ID"+str(sensorID)
    needDataFromSensor[sensorID] = True
    dataReady[sensorID] = False
    while(dataReady[sensorID] == False):
