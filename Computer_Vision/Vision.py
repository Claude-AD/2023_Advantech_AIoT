import cv2
from ultralytics import YOLO
from Crash import crash
from collections import deque
import copy

video = './dataset/test/cctv.gif'
cap = cv2.VideoCapture(video)

model = YOLO('./model/yolov8n.pt')

previous = []
sending = deque([])
accident_video = []
cnt = 0

def process_frame(fps):
    global previous, sending, accident_video, cnt, cap
    if not cap.isOpened():  # cap 객체가 열려있지 않다면
        cap = cv2.VideoCapture(video)  # cap 객체를 다시 초기화
        if not cap.isOpened():  # 여전히 열리지 않는다면
            return None, None, fps, None  # None을 반환하여 메인 루프 종료
    
    ret, frame = cap.read()
    if not ret:
        return None, None, fps, None  # No more frames or error
    
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    results = model.track(frame, persist=True, verbose=False)
    img = results[0].plot()
    white, previous, is_accident, plag = crash(results[0].boxes, img.shape, previous)
    
    sending.append([img])
    PLAG = None
    VIDEO = None
    if is_accident:
        cnt = 1
        accident_video.extend([*sending])
        PLAG = plag

    FRAME_LEN = 35 # repository of img files
    if cnt > 0:
        cnt += 1
        accident_video.append([img])
    if cnt >= FRAME_LEN:
        cnt = 0
        VIDEO = copy.deepcopy(accident_video)
        accident_video.clear()
    if len(sending) > FRAME_LEN:
        sending.popleft()

    if fps < FPS: # check of 1 second
        fps+=1
        return 0, PLAG, fps, VIDEO # non 1 second
    else:
        fps = 0
        return img, PLAG, fps, VIDEO # 1 second

