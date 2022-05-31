import socket
from pynput import keyboard
from threading import Thread
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print("Hostname:",host)
port = 8184
coordinates = []#player locations
bullets = []#bullet locations
serversocket.bind((host, port))
No_Clients = 0
clientsockets = {}
print("Once all users have connected, press SPACE to continue/play.")
def break_loop(key, abortKey='space'):
    try:
        k = key.char
    except:
        k = key.name
    if k == abortKey:
        return False
def infiniloop():
    global No_Clients,clientsockets,serversocket
    while True:
        clientsocket, addr = serversocket.accept()
        clientsockets[No_Clients] = clientsocket
        print("Got a connection from %s" % str(addr))
        No_Clients += 1
serversocket.listen()
listener = keyboard.Listener(on_press=break_loop, abortKey='space')
listener.start()
Thread(target=infiniloop, args=(), name='infiniloop', daemon=True).start()
listener.join()
print("Starting session...")
for turn in range(No_Clients):
    coordinates.append("")
for turn in range(No_Clients):
    bullets.append("")
clientSkip = []
running = True
while running:
    #checking players are alive and cutting connections
    #receiving locations from players
    for clientKey in clientsockets.keys():
        message = clientsockets[clientKey].recv(8192).decode()
        if message != "True":
            coordinates[clientKey] = message
        else:
            coordinates[clientKey] = "empty,"
            bullets[clientKey] = "empty,"
            clientsockets[clientKey].close()
            clientSkip.append(clientKey)
    for clientSkipped in clientSkip:
        clientsockets.pop(clientSkipped, None)
    clientSkip = []

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

    if len(clientsockets) == 0:
        running = False
print("Server shutting down...")
serversocket.close()