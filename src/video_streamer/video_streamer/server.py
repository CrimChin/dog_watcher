#!/usr/bin/env python

from importlib import import_module
import os
import rclpy
import cv2
from rclpy.context import Context
from rclpy.node import Node
from flask import Flask, render_template, Response
import signal, sys
from threading import Thread, Event
from rclpy.parameter import Parameter
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ServerSocket(Node):
    app = Flask(__name__)
    frame = None # Global variable frame (the holy image)

    # Objects of cvbridge and event
   
    def __init__(self):
        super().__init__("ServerSocket")
        self.sub = self.create_subscription(Image, "/model_image",self.get_frame,10)
        self.bridge = CvBridge()
        self.event = Event()
        self.event.set()

    def get_frame(self,msg):
        rclpy.spin_once(timeout_sec=1.0)
        self.cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding = "passthrough")
        frame = cv2.imencode(".jpg",self.cv_image)[1].tobytes()
        self.event.wait()
        self.event.clear()
        return frame

    @app.route('/')
    def index(self):
        """Video streaming home page."""
        return render_template('index.html')


    def gen_frames(self, camera):
        """Video streaming generator function."""
        yield b'--frame\r\n'
        while True:
            frame = self.get_frame()
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


    @app.route('/video_feed')
    def video_feed(self):
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(self.gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    def signal_handler(self, signal, frame):
        rclpy.shutdown()
        sys.exit(0)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', threaded=True, debug = True)