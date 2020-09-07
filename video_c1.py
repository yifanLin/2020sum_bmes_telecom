#client code for video transfer which pulls video from server 
import socket
import threading
import pickle
import datetime
from queue import Queue 

import cv2, numpy as np

SERVER_HOST = "192.168.1.82"
SERVER_PORT = 5050

TIME = datetime.datetime.now()
TIME = TIME.strftime("%m/%d/%Y, %H:%M:%S")

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.sock.connect((SERVER_HOST,SERVER_PORT))

        iThread = threading.Thread(target=self.prompt, name="aPromptTh")
        iThread.daemon = True
        iThread.start()

        while True:
            raw_data = Queue(maxsize = 10)
            while True:
                print("recev of c1 ongoing Starting another round...")
                if raw_data.full(): 
                    break
                raw_data.put(self.sock.recv(4096))
            print("recev of c1 finished!")
            print(raw_data)
            data = pickle.loads(raw_data)

            if data[1] == "eye":
                cv2.imshow("Window name",data[2])

            else:
                print(data)
            if not data:
                break
    

    def prompt(self):
        while True:
            command = input("client@a >")
            raw_data = ["a","command",command]
            self.send_data(raw_data)

#overwriting function send_data in threading.py file of Python lib
    def send_data(self,data):
         #while True:
        data = pickle.dumps(data)
        self.sock.sendall(data)

#pdb debugging
#import pdb; pdb.set_trace()
#print("trying to debug")
client = Client()