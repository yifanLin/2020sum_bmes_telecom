import socket
import threading
import pickle

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connections = []
    def __init__(self):
        self.sock.bind(('127.0.0.1', 1234))
        self.sock.listen(5)
        print("Server created")
    def handler(self, c, a):
        while True:
            try:
                raw_data = c.recv(1024)
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


def main():
    server = Server()
    server.run()

if __name__ == '__main__':
    while True:
        main()
