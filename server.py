import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname(socket.gethostname()), 7090))
s.listen()

print(f"Listening on {socket.gethostbyname(socket.gethostname())}")
clt, adr = s.accept()
print(f"Connection to {adr} established")
print(f"Connection from {clt}")

clt.send(bytes("count", "utf-8"))
