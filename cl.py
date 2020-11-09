import socket

HEADER = 64
PORT = 7070
SERVER = "76.95.189.45"
SERVER1 = "192.168.1.254"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"
ADDR = (SERVER1, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


connected = True
while connected:
    hmm = input("Enter your message: ")
    if hmm == DISCONNECT_MESSAGE:
        send("User disconnected.")
        connected = False
    send(hmm)

