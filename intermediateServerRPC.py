from inspect import signature
from os import path
import inspect
import intermediateServer
import socket
import json
import threading



def printError(msg):
    print(msg)
    exit()

class functionDetails:
    def __init__(self,name,args):
        self.name = name
        self.args = args
        #self.response = response

def functionExists(f: functionDetails):
    function_names = [func for func in dir(intermediateServer) if not func.startswith('__')]
    if f.name in function_names:
        return True
    return False

class RPC:
    functionsRegistered = []
    def registerFunctions(self,filePath):
        if not (path.exists(filePath)):
            printError(filePath+" does not exists")
        file1 = open(filePath,'r')
        Lines = file1.readlines()
        for  f in Lines:
            tokens = f.split()
            functionName = tokens[0]
            args = []
            for x in range(1,len(tokens)):
                args.append(tokens[x])
            func = functionDetails(functionName,args)
            if functionExists(func):
                self.functionsRegistered.append(func)
            else:
                printError(functionName + " does not exists in module")
    
def jsonify(functions):
    ans = ""
    for f in functions:
        ans += json.dumps(vars(f)) + '$'
    ans = ans[:-1]
    return ans

def handleRPCConn(s,rpc):
    while True:
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print("recvd form client",data)
                if not data:
                    break
                elif data == b'getFunctions':
                    funcNamesJson = jsonify(rpc.functionsRegistered)
                    conn.sendall(str.encode(funcNamesJson))
                else:
                    data = data.decode('utf-8')
                    funcDetails = json.loads(data)
                    print(funcDetails)
                    methodToCall = getattr(intermediateServer,funcDetails['name']) #add
                    ans = methodToCall(*funcDetails['args']) # 
                    conn.sendall(str.encode(str(ans)))

def handleReversePoll(spoll):
    while True:
        conn, addr = spoll.accept()

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024) # will recieve sensor id can be 1 and 2
                sensorID = int(data)
                if(sensorID != 1 or sensorID != 2):
                    print("This sensor is not registered with intermediate server")
                    conn.sendall(str.encode("no"))
                elif(intermediateServer.needDataFromSensor[sensorID] == True):
                    conn.sendall(str.encode("fetch data"))
                    sensorData = conn.recv(1024)
                    intermediateServer.sensorData[sensorID] = sensorData
                    intermediateServer.dataReady[sensorID] = True
                else:
                    conn.sendall(str.encode("no"))
                

def main():
    rpc = RPC()
    rpc.registerFunctions("functionNames.txt")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    PORT = 12345
    s.bind(('127.0.0.1',PORT))
    s.listen()
    t1 = threading.Thread(target=handleRPCConn,args=(s,rpc,))
    t1.start()

    spoll = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    PORTReversePoll = 12346
    spoll.bind(('127.0.0.1',PORTReversePoll))
    s.listen()
    t2 = threading.Thread(target=handleReversePoll,args=(spoll))
    t2.start()

    

if __name__ == "__main__":
    main()
