import socket
import cv2
import pickle
import struct

class WebClient():
    def __init__(self) -> None:
        
        # create socket
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_ip = '192.168.1.20' # paste your server ip address here
        self.port = 7777
        self.data = b""
        self.payload_size = struct.calcsize("Q")
    
    def client_connect(self):
        self.client_socket.connect((self.host_ip,self.port)) # a tuple
        
        while True:
            while len(data) < self.payload_size:
                packet = self.client_socket.recv(4*1024) # 4K
                if not packet: break
                data+=packet
            packed_msg_size = data[:self.payload_size]
            data = data[self.payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += self.client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("RECEIVING VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            if key  == ord('q'):
                break
        self.client_socket.close()