import socket, cv2, pickle, struct

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = ''
print('HOST IP:', host_ip)
port = 5060
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)
data = b""
payload_size = struct.calcsize("Q")

client_socket, addr = server_socket.accept()
print('GOT CONNECTION FROM:', addr)
if client_socket:
    while True:
        #Finds length of payload and adds payload to variable data
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size] #Defines the first 8 integers of data as the size
        data = data[payload_size:] #Defines everything remainig in the data as the data for the image

        msg_size = struct.unpack("Q", packed_msg_size)[0] #Divides array based on msg size/8 (mirrors server code)

        #Adjust reading frame based on message size, msg sized based on "Q" for byte length. Adds recv msg to string data
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)
        frame_data = data[:msg_size] #Defines one length of msg as the frame data
        data = data[msg_size:] #Adds remaining data to the next image element
        frame = pickle.loads(frame_data) #Unpickles data and adds to frame object
        cv2.imshow("RECEIVING VIDEO", frame) #Shows frame and video
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        server_socket.close()

