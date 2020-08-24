import socket
import threading
import pickle

SERVER_HOST = "192.168.1.82"
SERVER_PORT = 5050

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connections = []
    def __init__(self):
        self.sock.bind((SERVER_HOST, SERVER_PORT))
        self.sock.listen(5)
        print("Server created")

    def handler(self, c, a):
        #pdb debugging
        #import pdb; pdb.set_trace()
        #print("trying to debug server's handler")
        while True:
            try:
                #recv data from sending client (video_c.py)
                raw_data = c.recv(1024)
                #trying to receive multiple packets which are all together unpacked into an image

            except ConnectionResetError:
                print("Error")
                print(str(a[0]) + ':' + str(a[1]), "disconnected roughly")
                self.connections.remove(c)
                c.close()
                break
            except:
                print("Error while recieving data")
                continue

            for connection in self.connections:
                #while c is the sending client, the following 2 lines sendall data to command client
                if connection != c:
                    connection.sendall(raw_data)
            if not raw_data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        print("Server is running")
        while True:
            try:
                c, a = self.sock.accept()
                print(str(a[0]) + ':' + str(a[1]), "connected")
            except:
                print("Error during client connection")
                continue
            cThread = threading.Thread(target=self.handler, args=(c, a), name="HandlerTh")
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            #self.handler(self, (c,a))


def main():
    #pdb debugging
    #import pdb; pdb.set_trace()
    #print("trying to debug server's recev")
    server = Server()
    server.run()

if __name__ == '__main__':
    while True:
        main()
