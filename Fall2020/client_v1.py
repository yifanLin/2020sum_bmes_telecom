# File header: The following script receives a very simple message from this server to whatever client it connects to
# Contributor: Jay Golden, Aayush Somani, Yifan Lin
# latest update: 11/01/2020

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client connects to a certain server ip and port
s.connect(('SERVER_IP', 5050))
# ask the client to receive message, with a buffer size of     # 1024
msg=s.recv(1024)
# decode the msg with what it was originally encoded, which    # is utf-8 in this case
print(msg.decode("utf-8"))
