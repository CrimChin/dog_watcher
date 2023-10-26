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
        self.pose_pub = self.create_publisher()
        self.model = YOLO("yolo_training/runs/detect/train/weights/best.onnx")
        self.middle_range = [300,340]

    def listener_callback(self, msg):
        try:
            img_msg = self.bridge.imgmsg_to_cv2(msg)
            results = self.model.predict(source=img_msg, show=True, classes=16, conf=0.6, verbose= False)
            for r in results:
                boxes = r.boxes.xyxy
                for box in boxes:
                    middle_detection = (box[0] + box[2])/2
                    if min(self.middle_range) < middle_detection < max(self.middle_range):
                        self.get_logger().info("YOURE IN THE MIDDLE")
                    elif min(self.middle_range) > middle_detection:
                        self.get_logger().info("MOVE LEFT")
                    elif max(self.middle_range) < middle_detection:
                        self.get_logger().info("MOVE RIGHT")

                        
                

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

