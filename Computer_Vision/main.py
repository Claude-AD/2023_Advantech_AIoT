import cv2
from ultralytics import YOLO
from Crash import crash

model = YOLO('./model/yolov8n.pt')

video = './dataset/test/cctv.gif'
cap = cv2.VideoCapture(video)

previous = []
if cap.isOpened():
  while True:
    ret, frame = cap.read()
    results = model.track(frame, persist=True, verbose=False)
    img = results[0].plot()
    white, previous = crash(results[0].boxes, img.shape, previous)
    
    img = cv2.addWeighted(img, 1, white, 1, 0)
    #img = cv2.resize(img, dsize=(0,0), fx=0.5, fy=0.5)
    cv2.imshow('img', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
else:
  print("unable to use camera")