import socket 
import json
import sys

HOST = '127.0.0.1'
PORT = 12345

class callableFunc:
    def __init__(self,name,numberOfArgs,s):
        self.name = name
        self.numberOfArgs = numberOfArgs
        self.s = s # s is the socket
    def __call__(self,*args):
        if len(args) != self.numberOfArgs :
            print("incorrect args in " + self.name)
            exit()
        else:
            dict = {'name':self.name,'args':args}
            funArgs = json.dumps(dict)
            self.s.sendall(str.encode(funArgs))
            response = self.s.recv(1024).decode('utf-8')
            return response
            # need to connect to server pass the args then return the solution

class clientRPC:
    functionDetails = []
    def __init__(self,HOST,PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((HOST,PORT))
        s.sendall(b'getFunctions')
        data = s.recv(1024).decode('utf-8')
        data = data.split('$')
        for d in data:
            funcDetails = json.loads(d)
            newFunc = callableFunc(funcDetails['name'],len(funcDetails['args']),s)
            setattr(clientRPC,funcDetails['name'],newFunc)

def main():
    rpc = clientRPC(HOST,PORT)

if __name__ == "__main__":
    main()