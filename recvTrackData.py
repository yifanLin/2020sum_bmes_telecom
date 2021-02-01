import pickle
from socket import *

# Socket Create
socket = socket(AF_INET, SOCK_STREAM)

host_ip = gethostbyname(gethostname())
#host_ip = "192.168.0.1"
print('HOST IP:', host_ip)
port = 40005
socket_address = (host_ip, port)

socket.bind(socket_address)
socket.listen(5)
client_socket, addr = socket.accept()

if client_socket:
    while True:
        pickMsg = client_socket.recv(64)
        msg = pickle.loads(pickMsg)
        print(msg)
