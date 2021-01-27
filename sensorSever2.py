import socket 
import json
import sys
from random import seed
from random import randint

seed(1)
sensorID = '2'
INTERMEDIATE_HOST = '127.0.0.1'
INTERMEDIATE_PORT = 12346


def getSensorData():
    ans = ""
    for _ in range(10):
        value = randint(0,10)
        ans = ans+str(value)
    return ans
    
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((INTERMEDIATE_HOST,INTERMEDIATE_PORT))
    while True:
        s.sendall(sensorID.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        #print(data)
        if(data == "no"):
            continue
        elif(data == "fetch data"):
            sensorData = getSensorData()
            s.sendall(sensorData.encode('utf-8'))

if __name__ == "__main__":
    main()