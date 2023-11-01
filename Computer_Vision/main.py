import cv2
from ultralytics import YOLO
from Crash import crash
from Car_Manager import plag
from collections import deque

model = YOLO('./model/yolov8n.pt')

# video = './dataset/test/part2.mp4'
video = './dataset/test/cctv.gif'
cap = cv2.VideoCapture(video)

previous = []
sending = deque([])
accident_video = []
cnt = 0

if cap.isOpened():
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  fps = int(cap.get(cv2.CAP_PROP_FPS))
  w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  # out = cv2.VideoWriter('1.mp4', fourcc, fps, (w, h))
  
  while True:
    
    ret, frame = cap.read()
    if ret == 0 or (cv2.waitKey(1) & 0xFF == ord('q')):
      break
    
    results = model.track(frame, persist=True, verbose=False)
    img = results[0].plot()
    white, previous, is_accident = crash(results[0].boxes, img.shape, previous)
    
    img = cv2.addWeighted(img, 1, white, 1, 0)
    # img = cv2.resize(img, dsize=(0,0), fx=0.5, fy=0.5)
    cv2.imshow('img', img)
    # out.write(img)
    
    
    if is_accident:
      sending.append([img, plag])
      cnt = 1
      accident_video.append([*sending])
    else:
      sending.append([img])  

    '''sending 보내기'''
    print(len(sending))
    
    if cnt > 0:
      cnt += 1
      accident_video.append([img])
    if cnt >= 5:
      cnt = 0
      '''accident_video[5:] 보내기'''
      accident_video.clear()
      
    if len(sending) > 15:
      sending.popleft()
      
  # pd_data = pd.DataFrame(data)
  # pd_data.to_csv('test.csv')
  # out.release()

else:
  print("unable to use camera")