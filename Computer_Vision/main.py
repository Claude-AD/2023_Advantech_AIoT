from Vision import process_frame
from datahub.Data import receive_plag_data
from datahub.EdgeAgent import generate_edgeAgent, sendDataToDataHub
import cv2, time
from post import upload_image, upload_mp4

import pyaudio
import time
import numpy as np

# Audio Stream Settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def main():
    edge_agent = generate_edgeAgent()  # EdgeAgent 인스턴스 생성 및 설정
    fps = 0

    # Start PyAudio
    audio = pyaudio.PyAudio()

    # Open Stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, 
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    # Variable to store sound level
    sound_level_list = []
    last_time = time.time()

    while True:
        ##### ---------- sound ---------- #####
        current_time = time.time()
        over_threshold = False

        if current_time - last_time >= 1:
            sound_level_average = np.mean(sound_level_list)
            if sound_level_average >= 500:
                over_threshold = True

            print(f'Sound Level during 1sec: {sound_level_average}') ##### Have to fix this code to sending data to Datahub #####
            sound_level_list = []
            last_time = current_time

        # Read audio stream data
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)

        # Calculate mean sound level
        sound_level = np.average(np.abs(data))
        sound_level_list.append(sound_level)

        ##### --------- VISION ---------- #####
        img, plag, fps, video = process_frame(fps)  # img와 plag 혹은 img와 None을 받음

        if img is None and plag is None: # img, plag 둘 다 None이면 영상이 끝난것이니 종료
            print("No more frames to process or unable to open video. Exiting.")
            break
        elif img is 0: # 1초가 지나지 않았을 때
            pass
        else:          # 1초(30프레임)마다 사진 보내기
            upload_image(img)   #'''img 보내기'''
            # cv2.imshow("img", img)
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     break
            
        if plag is not None: # plag가 None이 아닌 것이 리턴된거면 is_accident이니 처리
            # 사고가 감지되었을 때 처리
            print(f"Accident detected, processing plag data: {plag}") # 요 출력문 나오면서 plag 처리함
            edge_data = receive_plag_data(plag)  # Data.py를 통해 EdgeData로 변환
            sendDataToDataHub(edge_agent, edge_data)  # 변환된 EdgeData를 EdgeAgent.py를 통해 데이터 허브로 전송

        if video is not None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            f = 30.0
            h, w, l = video[0][0].shape
            out = cv2.VideoWriter('output.mp4', fourcc, f, (w, h))
            for i in range(len(video)):
                out.write(video[i][0])
            out.release()
            
            upload_mp4('./output.mp4') #'''./output.mp4 보내기'''
            # time.sleep(5)   # 5초간 기다리기

if __name__ == "__main__":
    main()
