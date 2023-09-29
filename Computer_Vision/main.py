import cv2
import numpy as np
from ultralytics import YOLO
from itertools import combinations

from Crash import crash

model = YOLO('./model/yolov8n.pt')

video = './dataset/test/cctv.gif'
cap = cv2.VideoCapture(video)

if cap.isOpened():
  while True:
    ret, frame = cap.read()
    results = model.track(frame, persist=True)
    processed_img = results[0].plot()
    
    processed_img = cv2.addWeighted(processed_img, 1, crash(results[0].boxes, processed_img.shape), 1, 0)
    processed_img = cv2.resize(processed_img, dsize=(0,0), fx=0.5, fy=0.5)
    cv2.imshow('img', processed_img)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
else:
  print("unable to use camera")