import socket
import cv2
import pickle
import struct

class Webserver():
    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        port = 7777
        self.socket_address = (host_ip,port)
        

    def server_connect(self):
        self.server_socket.bind(self.socket_address)
        self.server_socket.listen(5)
        
        while True:
            client_socket,addr = self.server_socket.accept()
            if client_socket:
                vid = cv2.VideoCapture(0)
                while vid.isOpen():
                    img,frame = vid.read()
                    a = pickle.dumps()
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)
                    
                    cv2.imshow('TRANSMITTING VIDEO',frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key ==ord('q'):
                        client_socket.close()