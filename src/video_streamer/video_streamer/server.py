from typing import List
import rclpy
from rclpy.context import Context
from rclpy.node import Node
import cv2 
import imutils 
import socket
import numpy as np
import time
import base64

from rclpy.parameter import Parameter
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

BUFF_SIZE = 65536

class ServerSocket(Node):
    def __init__(self):
        super().__init__("ServerSocket")
       
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        port = 9999
        self.socket_address = (host_ip,port)
        self.server_socket.bind(self.socket_address)
        print('Listening at:',self.socket_address)

        self.create_subscription(Image, "/model_image",self.stream_video,10)
        self.bridge = CvBridge()
    
    def stream_video(self,msg):
        vid = self.bridge.imgmsg_to_cv2(msg) 
        fps,st,frames_to_count,cnt = (0,0,20,0)

        while True:
            self.get_logger().info("IN THE LOOP")
            gram,client_addr = self.server_socket.recvfrom(BUFF_SIZE)
            self.get_logger().info('GOT connection from ',client_addr)
            WIDTH=400
            while True:
                _,frame = vid.read()
                frame = imutils.resize(frame,width=WIDTH)
                encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
                message = base64.b64encode(buffer)
                self.server_socket.sendto(message,client_addr)
                frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                cv2.imshow("Transmitting Frame", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.server_socket.close()
                    break
                if cnt == frames_to_count:
                    try:
                        fps = round(frames_to_count/(time.time()-st))
                        st=time.time()
                        cnt=0
                    except:
                        pass
                cnt+=1

def main(args=None):
    rclpy.init(args=args)

    server = ServerSocket()
    rclpy.spin(server)

    server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()