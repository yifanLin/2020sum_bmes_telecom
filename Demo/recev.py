import pickle
from socket import *
import os

# Socket Create
socket = socket(AF_INET, SOCK_STREAM)

#host_ip = gethostbyname(gethostname())
# empty host_ip accepts all connections (wildcard)
host_ip = ""
print('HOST IP:', gethostname())
port = 5075 # make sure port number matches the one in SendCoords.py
socket_address = (host_ip, port)

socket.bind(socket_address)
socket.listen(5)
client_socket, addr = socket.accept()

counter = 0

if client_socket:
    while True:
        pickMsg = client_socket.recv(4096)
        if pickMsg is not None:
            msg = pickle.loads(pickMsg)
            print(msg)