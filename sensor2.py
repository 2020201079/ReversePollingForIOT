import socket 
import time
from random import seed
from random import randint

seed(1)
INTERMEDIATE_HOST = '127.0.0.1'
INTERMEDIATE_PORT = 34568

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((INTERMEDIATE_HOST,INTERMEDIATE_PORT))
    while True:
        time.sleep(8) # 5 sec delay
        value = randint(0, 10)
        value = str(value)
        s.sendall(value.encode('utf-8'))


if __name__ == "__main__":
    main()