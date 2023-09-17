#!/usr/bin/python3

from typing import List
import rclpy
from rclpy.context import Context
from rclpy.node import Node
import cv2
import numpy as np
from cam_hardware.utils import plot_bboxes
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO

class ImageProcessing(Node):
    def __init__(self):
        super().__init__("image_processing")
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, "/image", self.listener_callback,10)
        self.model = YOLO("runs/detect/train9/weights/best.onnx")
    
    def listener_callback(self, msg):
        try:
            img_msg = self.bridge.imgmsg_to_cv2(msg)
            results = self.model.predict(source=img_msg, show=True)

        except CvBridgeError as e:
            print(f"THIS IS ERROR: {e}")
            

def main(args=None):
    rclpy.init(args=args)

    image_processer = ImageProcessing()
    print("Listening")
    rclpy.spin(image_processer)

    image_processer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

