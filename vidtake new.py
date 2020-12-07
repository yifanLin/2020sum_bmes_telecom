import socket, cv2, pickle, struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "76.95.185.15"  #Server IP
port = 8070
client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")


while True:
    vid = cv2.VideoCapture(0)

    while (vid.isOpened()):
         img, frame = vid.read()
         a = pickle.dumps(frame)
         message = struct.pack("Q", len(a)) + a #Divide the message into len(a)/8 segments and store as an array
         client_socket.sendall(message) #Repeatedly send the elements of message

         cv2.imshow('TRANSMITTING VIDEO', frame) #Shows transmission video as example
         key = cv2.waitKey(1) & 0xFF
         if key == ord('q'): #Included in the cv2 examples, probably does something important
            client_socket.close()
