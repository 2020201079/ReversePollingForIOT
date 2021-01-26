from clientRPC import clientRPC

HOST = '127.0.0.1'
PORT = 12345

rpc = clientRPC(HOST,PORT)
ans = rpc.fetchData(1)

print(ans)