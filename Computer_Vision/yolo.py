import cv2
from ultralytics import YOLO
from itertools import combinations
import numpy as np
from tracing import car

model = YOLO('./model/yolov8n.pt')

video = './video/night.mp4'
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
    distance = np.linalg.norm(np.array(p1) - np.array(p2))

    sums = 0
    for i in range(2,4):
      sums += cordi[n1][i]
      sums += cordi[n2][i]
    threshold = sums/4

    if distance < threshold*2:
      id1 = int(ids[n1].item())-1
      id2 = int(ids[n2].item())-1
      if cars[id1] == 0:
        cars[id1] = car(p1[0], p1[1])
        continue
      if cars[id2] == 0:
        cars[id2] = car(p2[0], p2[1])
        continue
      
      ret1, white = cars[id1].trace(p1[0], p1[1], white, threshold, p2)
      ret2, white = cars[id2].trace(p2[0], p2[1], white, threshold, p1)
      
      if distance < threshold and (ret1 or ret2):
        for i in range(15): print("ACCIDENT")
  return white



def accident2(boxes, shape):
  cordi = boxes.xywh
  ids = boxes.id
  white = np.zeros(shape, dtype=np.uint8)

  n = len(cordi)
  if n <= 1 or ids == None:
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