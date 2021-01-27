from collections import defaultdict

needDataFromSensor = defaultdict(bool) # a dic with sensorid -> bool
dataReady = defaultdict(bool) # a dic with sensorid -> bool
sensorData = defaultdict(str) # a dic with sensorid -> data

def fetchData(sensorID):
    #return "Fetch data is called with sensor ID"+str(sensorID)
    print("fetch data called with sensorID : ", sensorID)
    needDataFromSensor[sensorID] = True
    dataReady[sensorID] = False
    while(dataReady[sensorID] == False):
        pass
    needDataFromSensor[sensorID] = False
    dataReady[sensorID] = False
    ans = sensorData[sensorID]
    sensorData[sensorID] = ""
    return ans