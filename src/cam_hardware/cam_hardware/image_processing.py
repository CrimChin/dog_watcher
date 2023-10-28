#!/usr/bin/python3

from typing import List
import rclpy
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
        self.sub = self.create_subscription(Image, "/image", self.run_prediction,10)
        self.pose_pub = self.create_publisher(Image, "/model_image", 10)
        self.model = YOLO("yolo_training/runs/detect/train/weights/best.onnx")

    def run_prediction(self, msg):
        try:
            img_msg = self.bridge.imgmsg_to_cv2(msg)
            results = self.model.predict(source=img_msg, show=False, classes=16, conf=0.6, verbose= False)
            self.pose_pub.publish(self.bridge.cv2_to_imgmsg(results[0].plot()))
        
        except CvBridgeError as e:
            print(f"THIS IS ERROR: {e}")
        
        return results
    
    def track_dog(self,results):
            results = self.run_prediction()
            middle_range = [300,340]

            for r in results:
                boxes = r.boxes.xyxy
                for box in boxes:
                    middle_detection = (box[0] + box[2])/2
                    if min(middle_range) < middle_detection < max(middle_range):
                        self.get_logger().info("YOURE IN THE MIDDLE")
                    elif min(middle_range) > middle_detection:
                        self.get_logger().info("MOVE LEFT")
                    elif max(middle_range) < middle_detection:
                        self.get_logger().info("MOVE RIGHT")
            
                
            

def main(args=None):
    rclpy.init(args=args)

    image_processer = ImageProcessing()
    print("Listening")
    rclpy.spin(image_processer)

    image_processer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

