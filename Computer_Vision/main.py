import cv2
from ultralytics import YOLO
from Crash import crash
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
    white, previous, is_accident, plag = crash(results[0].boxes, img.shape, previous)
    
    img = cv2.addWeighted(img, 1, white, 1, 0)
    # cv2.imshow('img', img)
    # out.write(img)
    
    
    if is_accident:
      sending.append([img, plag])
      cnt = 1
      accident_video.extend([*sending])
    else:
      sending.append([img])  

    '''sending 보내기'''
    
    FRAME_LEN = 30
    if cnt > 0:
      cnt += 1
      accident_video.append([img])
    
    if cnt >= FRAME_LEN:
      cnt = 0
      ########
      for i in range(len(accident_video)):
        cv2.imshow('img', accident_video[i][0])
        if ret == 0 or (cv2.waitKey(1) & 0xFF == ord('q')):
          break
      ########
      
      '''accident_video 보내기'''
      accident_video.clear()
      
    if len(sending) > FRAME_LEN:
      sending.popleft()
      
  # pd_data = pd.DataFrame(data)
  # pd_data.to_csv('test.csv')
  # out.release()

else:
  print("unable to use camera")