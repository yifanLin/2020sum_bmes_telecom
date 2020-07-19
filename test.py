import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('66.75.250.79', 5050))

msg=s.recv(1024)
print(msg.decode("utf-8"))
