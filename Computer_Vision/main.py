import cv2
from ultralytics import YOLO
from itertools import combinations
import numpy as np
from tracing import car

model = YOLO('./model/yolov8n.pt')

video = './dataset/test/night.gif'
cap = cv2.VideoCapture(video)

cars = []
def accident(boxes, shape):
  cordi = boxes.xywh
  ids = boxes.id
  white = np.zeros(shape, dtype=np.uint8)

  n = len(cordi)
  if n <= 1 or ids == None:
    return white
  global cars
  if len(cars) < int(ids.max().item()):
    for _ in range(int(ids.max().item()) - len(cars)):
      cars.append(0)

  arr = [i for i in range(n)]
  arr = list(combinations(arr, 2))

  for n1, n2 in arr:
    p1 = (int(cordi[n1][0].item()), int(cordi[n1][1].item()))
    p2 = (int(cordi[n2][0].item()), int(cordi[n2][1].item()))
    
    th_w = cordi[n1][2]/2 + cordi[n2][2]/2
    th_h = cordi[n1][3]/2 + cordi[n2][3]/2
    
    if np.abs(p1[0]-p2[0]) < th_w and np.abs(p1[1]-p2[1]) < th_h:
      for i in range(15): print("OVERLAP")
  return white


if cap.isOpened():
  while True:
    ret, frame = cap.read()
    results = model.track(frame, persist=True)  
    processed_img = results[0].plot()
    
    processed_img = cv2.addWeighted(processed_img, 1, accident(results[0].boxes, processed_img.shape), 1, 0)
    cv2.imshow('img', processed_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
else:
  print("unable to use camera")