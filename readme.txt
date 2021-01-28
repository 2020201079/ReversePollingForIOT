Steps to run

1) Run the intermediateServerRPC.py first
2) Run the sensorServer.py
3) Run sensor1.py and sensor2.py
4) sensorServer starts printing the values it recieved from sensor1 and sensor2
5) in the client set the sensorID as 1 or 2 (whatever sensor) run client.py --> client will print the data it fetched


Sensor server keeps polling intermediate server if there is any request

communcation between client and intermediate server is using rpc