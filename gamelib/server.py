import socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print("Hostname:",host)
port = 8184
coordinates=[]#player locations
bullets=[]#bullet locations
serversocket.bind((host, port))
No_Clients=int(input("How Many Clients?\n>: "))#waits for that number of clients, no contingency for extra clients
serversocket.listen(No_Clients)
for turn in range(No_Clients):
    coordinates.append("")
for turn in range(No_Clients):
    bullets.append("")
if No_Clients>0:
    clientsocket0,addr0 = serversocket.accept()
    print("Got a connection from %s" % str(addr0))
client0=True#upon death sets to false
if No_Clients>1:
    clientsocket1,addr1 = serversocket.accept()
    print("Got a connection from %s" % str(addr1))
client1=True#upon death sets to false
if No_Clients>2:
    clientsocket2,addr2 = serversocket.accept()
    print("Got a connection from %s" % str(addr2))
client2=True#upon death sets to false
if No_Clients>3:
    clientsocket3,addr3 = serversocket.accept()
    print("Got a connection from %s" % str(addr3))
client3=True#upon death sets to false
if No_Clients>4:
    clientsocket4,addr4 = serversocket.accept()
    print("Got a connection from %s" % str(addr4))
client4=True#upon death sets to false
while True:
    #checking players are alive and cutting connections
    #receiving locations from players
    if No_Clients>0 and client0:
        message=clientsocket0.recv(8192).decode()
        if message!="True":
            coordinates[0]=message
        else:
            client0=False
    elif not client0:
        coordinates[0]="0,900,"
        clientsocket0.close()
    if No_Clients>1 and client1:
        message=clientsocket1.recv(8192).decode()
        if message!="True":
            coordinates[1]=message
        else:
            client1=False
    elif not client1:
        coordinates[1]="0,900,"
        clientsocket1.close()
    if No_Clients>2 and client2:
        message=clientsocket2.recv(8192).decode()
        if message!="True":
            coordinates[2]=message
        else:
            client2=False
    elif not client2:
        coordinates[2]="0,900,"
        clientsocket2.close()
    if No_Clients>3 and client3:
        message=clientsocket3.recv(8192).decode()
        if message!="True":
            coordinates[3]=message
        else:
            client3=False
    elif not client3:
        coordinates[3]="0,900,"
        clientsocket3.close()
    if No_Clients>4 and client4:
        message=clientsocket4.recv(8192).decode()
        if message!="True":
            coordinates[4]=message
        else:
            client4=False
    elif not client4:
        coordinates[4]="0,900,"
        clientsocket4.close()
    #sending player the locations of others
    if No_Clients>0 and client0:
        word=""
        for coord in coordinates:
            word+=coord
        clientsocket0.send(word.encode())
    if No_Clients>1 and client1:
        word=""
        for coord in coordinates:
            word+=coord
        clientsocket1.send(word.encode())
    if No_Clients>2 and client2:
        word=""
        for coord in coordinates:
            word+=coord
        clientsocket2.send(word.encode())
    if No_Clients>3 and client3:
        word=""
        for coord in coordinates:
            word+=coord
        clientsocket3.send(word.encode())
    if No_Clients>4 and client4:
        word=""
        for coord in coordinates:
            word+=coord
        clientsocket4.send(word.encode())
    #receiving bullet locations from players
    if No_Clients>0 and client0:
        something=clientsocket0.recv(8192).decode()
        if something=="empty":
            bullets[0]="empty,"
        else:
            bullets[0]=something
    elif No_Clients>0:
        bullets[0]="empty,"
    if No_Clients>1 and client1:
        something=clientsocket1.recv(8192).decode()
        if something=="empty":
            bullets[1]="empty,"
        else:
            bullets[1]=something
    elif No_Clients>1:
        bullets[1]="empty,"
    if No_Clients>2 and client2:
        something=clientsocket2.recv(8192).decode()
        if something=="empty":
            bullets[2]="empty,"
        else:
            bullets[2]=something
    elif No_Clients>2:
        bullets[2]="empty,"
    if No_Clients>3 and client3:
        something=clientsocket3.recv(8192).decode()
        if something=="empty":
            bullets[3]="empty,"
        else:
            bullets[3]=something
    elif No_Clients>3:
        bullets[3]="empty,"
    if No_Clients>4 and client4:
        something=clientsocket4.recv(8192).decode()
        if something=="empty":
            bullets[4]="empty,"
        else:
            bullets[4]=something
    elif No_Clients>4:
        bullets[4]="empty,"
    #sending player the locations of others' bullets
    if No_Clients>0 and client0:
        word=""
        for coord in bullets:
            word+=coord
        clientsocket0.send(word.encode())
    if No_Clients>1 and client1:
        word=""
        for coord in bullets:
            word+=coord
        clientsocket1.send(word.encode())
    if No_Clients>2 and client2:
        word=""
        for coord in bullets:
            word+=coord
        clientsocket2.send(word.encode())
    if No_Clients>3 and client3:
        word=""
        for coord in bullets:
            word+=coord
        clientsocket3.send(word.encode())
    if No_Clients>4 and client4:
        word=""
        for coord in bullets:
            word+=coord
        clientsocket4.send(word.encode())
