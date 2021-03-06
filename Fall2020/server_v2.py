# File header: The following script recursively sends a very simple increasing integer message
# from this server to whatever client it connects to
# Contributor: Jay Golden, Aayush Somani, Yifan Lin
# latest update: 11/01/2020

# import socket package
import socket
# create a socket handle (object) to work with, and setting # up port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname(socket.gethostname()), 5050))
# enable socket object to listen and wait for clients to    # come in
s.listen()
# print notification msg about the state of server
print(f"Listening on {socket.gethostbyname(socket.gethostname())}")
# clt and adr capture client details as server accepts
clt, adr = s.accept()
# msg notification
print(f"Connection to {adr} established")
print(f"Connection from {clt}")
# server sending message, count original set to be 0
count = 0
while True:
    clt.send(bytes(str(count), "utf-8"))
    # increasing count in every loop
    count += 1
