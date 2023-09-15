#!/usr/bin/python3
from typing import List
import rclpy
from rclpy.context import Context
from rclpy.node import Node
import cv2
from rclpy.parameter import Parameter
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImageProcessing(Node):
    def __init__(self):
        super().__init__("image_processing")
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, "/image", self.listener_callback,10)
    
    def listener_callback(self, msg):
        try:
            img_msg = self.bridge.imgmsg_to_cv2(msg)
            self.get_logger().info(f'I heard {img_msg}')
        except CvBridgeError as e:
            print(e)
            

def main(args=None):
    rclpy.init(args=args)

    image_processer = ImageProcessing()
    print("Listening")
    rclpy.spin(image_processer)

    image_processer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

