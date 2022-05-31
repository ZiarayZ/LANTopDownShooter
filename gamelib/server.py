import socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print("Hostname:",host)
port = 8184
coordinates = []#player locations
bullets = []#bullet locations
serversocket.bind((host, port))
No_Clients = 0
clientsockets = {}
print("Once all users have connected, press CTRL + C to continue/play.")
try:
    while True:
        clientsocket, addr = serversocket.accept()
        clientsockets[No_Clients] = clientsocket
        print("Got a connection from %s" % str(addr))
        No_Clients += 1
except KeyboardInterrupt:
    pass
serversocket.listen(No_Clients)
for turn in range(No_Clients):
    coordinates.append("")
for turn in range(No_Clients):
    bullets.append("")
while True:
    #checking players are alive and cutting connections
    #receiving locations from players
    for clientKey in clientsockets.keys():
        message = clientsockets[clientKey].recv(8192).decode()
        if message != "True":
            coordinates[clientKey] = message
        else:
            coordinates[clientKey] = "0,900,"
            bullets[clientKey] = "empty,"
            clientsockets[clientKey].close()
            clientsockets.pop(clientKey, None)

    #sending player the locations of others
    for clientKey in clientsockets.keys():
        word = ""
        for coord in coordinates:
            word += coord
        clientsockets[clientKey].send(word.encode())

    #receiving bullet locations from players
    for clientKey in clientsockets.keys():
        something = clientsockets[clientKey].recv(8192).decode()
        if something == "empty":
            bullets[clientKey] = "empty,"
        else:
            bullets[clientKey] = something

    #sending player the locations of others' bullets
    for clientKey in clientsockets.keys():
        word = ""
        for coord in bullets:
            word += coord
        clientsockets[clientKey].send(word.encode())