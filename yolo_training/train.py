#!/usr/bin/python3

from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2

class ModelTrainer():
    def __init__(self) -> None:
        self.model = YOLO("yolov8n.pt")

    def train_model(self):
        self.model.train(data="/home/chinedu/dog_watcher/yolo_training/config.yaml", epochs=200)  # train the model
        metrics = self.model.val()
        path = self.model.export(format="onnx")
        # results = model("https://ultralytics.com/images/bus.jpg")
        # print(results)
    
    def get_image(self):
        image = Image.open(r"/home/chinedu/training_data/images/train/IMG_2666.JPG")
        image = np.asarray(image)
        result = self.model.predict(image)

        # print(result[0].boxes.data)
        self.plot_bboxes(image,result[0].boxes.data,score=False)    
            
if __name__ == '__main__':
    mt = ModelTrainer()
    mt.train_model()
    # mt.get_image()