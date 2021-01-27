from clientRPC import clientRPC

INTERMEDIATE_HOST = '127.0.0.1'
INTERMEDIATE_PORT = 12345
sensorID = 1
rpc = clientRPC(INTERMEDIATE_HOST,INTERMEDIATE_PORT)
ans = rpc.fetchData(sensorID)

print(ans)