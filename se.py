import socket
import threading

HEADER = 64
PORT = 7070
SERVER = "76.95.189.45"  # my public ip
SERVER2 = socket.gethostname()  # gets public ip
SERVER3 = ''  # empty string
SERVER4 = socket.gethostbyname(socket.gethostname())  # gets local ip
ADDR = (SERVER4, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(2048).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            break
        print(f"[{addr}] {msg}")
        conn.send("Message Received!".encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER4}")
    conn, addr = server.accept()
    handle_client(conn, addr)


print("[STARTING] server is starting...")
start()
