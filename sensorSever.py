import socket 
import json
import sys
import threading

INTERMEDIATE_HOST = '127.0.0.1'
INTERMEDIATE_PORT = 12346


sensor1data = []
sensor2data = []
lockSensor1 = threading.Lock()
lockSensor2 = threading.Lock()

def startSensor1(s,sensor1data):
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                data = data.decode('utf-8')
                lockSensor1.acquire()
                sensor1data.append(str(data))
                print("sensor1data : ",sensor1data)
                #print("sensor2data in thread 1 : ",sensor2data)
                lockSensor1.release()

def startSensor2(s,sensor2data):
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                data = data.decode('utf-8')
                lockSensor2.acquire()
                sensor2data.append(str(data))
                print("sensor2data : ",sensor2data)
                #print("sensor1data in thread 2 :",sensor1data)
                lockSensor2.release()

def getSensorData(id,sensor1data,sensor2data):
    if(id == 1):
        lockSensor1.acquire()
        ans = ''.join(sensor1data)
        sensor1data.clear()
        lockSensor1.release()
        return ans
    else:
        lockSensor2.acquire()
        ans = ''.join(sensor2data)
        sensor2data.clear()
        lockSensor2.release()
        return ans

def main():
    PORT_Sensor1 = 34567
    sSensor1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sSensor1.bind(('127.0.0.1',PORT_Sensor1))
    sSensor1.listen()
    t1 = threading.Thread(target=startSensor1,args=(sSensor1,sensor1data,))
    t1.start()

    PORT_Sensor2 = 34568
    sSensor2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sSensor2.bind(('127.0.0.1',PORT_Sensor2))
    sSensor2.listen()
    t2 = threading.Thread(target=startSensor2,args=(sSensor2,sensor2data,))
    t2.start()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((INTERMEDIATE_HOST,INTERMEDIATE_PORT))
    while True:
        s.sendall("request".encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        #print(data)
        if(data == "no"):
            continue
        elif(data == "1"):
            sensorData = getSensorData(1,sensor1data,sensor2data)
            if sensorData == '':
                sensorData = "nothing new to fetch"
            s.sendall(sensorData.encode('utf-8'))
        elif(data == "2"):
            sensorData = getSensorData(2,sensor1data,sensor2data)
            if sensorData == '':
                sensorData = "nothing new to fetch"
            s.sendall(sensorData.encode('utf-8'))
        else:
            s.sendall("wrong sensor id".encode('utf-8'))

if __name__ == "__main__":
    main()