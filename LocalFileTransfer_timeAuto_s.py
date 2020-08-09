import socket
import time
import tqdm
import os

#SERVER_HOST = "76.95.189.45"
SERVER_HOST = "192.168.1.82"
SERVER_PORT = 5050
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen()
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

while True:
    tic = time.perf_counter()
    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    if(received != ""):
        filename, filesize = received.split(SEPARATOR)
    else:
        print("break")
        continue
    # remove absolute path if there is
    filename = os.path.basename(filename)
    #filename = filename + str(i)
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    toc = time.perf_counter()
    print(f"received in {toc - tic:0.4f} seconds")

# close the client socket
client_socket.close()
# close the server socket
s.close()


#msg sending testing code
# count = "1888888888888888"
# clt, adr = s.accept()
# print(f"Connection to {adr} established")
# print(f"Connection from {clt}")

# while True:
#     tic = time.perf_counter()
#     clt.send(f"{filename}{SEPARATOR}{filesize}".encode())
#     #clt.send(bytes(count, "utf-8"))
#     toc = time.perf_counter()
#     print(f"reached and replied in {toc - tic:0.4f} seconds")
