import socket
import tqdm
import os

# the ip address or hostname of the server, the receiver
host = "192.168.1.82"
# the port, let's use 5001
port = 5050
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!disconnect"
# ADDR = (SERVER, PORT)
BUFFER_SIZE = 4096

s = socket.socket()
#Connecting to the server:
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

filename = "testBig.tsv"
filesize = os.path.getsize(filename)
SEPARATOR = "<SEPARATOR>"

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()
