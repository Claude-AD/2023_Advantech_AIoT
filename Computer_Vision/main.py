from Vision import process_frame
from datahub.Data import receive_plag_data
from datahub.EdgeAgent import generate_edgeAgent, sendDataToDataHub
import cv2, time, os
import numpy as np
import pyaudio, time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX = 0
is_on = False

import subprocess
def main():
    edge_agent = generate_edgeAgent()
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, 
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    sound_level_list = []
    last_time = time.time()
    
    cnt = 0
    while True:
        #######################################
        ##### ---------- sound ---------- #####
        
        current_time = time.time()
        over_threshold = False

        if current_time - last_time >= 1:
            sound_level_average = np.mean(sound_level_list)
            edge_data = receive_plag_data(sound_level_average, "Device2")  # Data.py를 통해 EdgeData로 변환
            sendDataToDataHub(edge_agent, edge_data)
            if sound_level_average >= 60:
                over_threshold = True

            print(f'Sound Level during 1sec: {sound_level_average}') ##### Have to fix this code to sending data to Datahub #####
            sound_level_list = []
            last_time = current_time

        # Read audio stream data
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)

        # Calculate mean sound level
        sound_level = np.average(np.abs(data))
        sound_level_list.append(sound_level)
        
        ##### ---------- sound ---------- #####
        #######################################

        #######################################
        ##### --------- VISION ---------- #####
        
        img, plag, video = process_frame()  # img와 plag 혹은 img와 None을 받음
        
        if img is None and plag is None: # img, plag 둘 다 None이면 영상이 끝난것이니 종료
            print("No more frames to process or unable to open video. Exiting.")
            break
        
        print(plag)
        show = cv2.resize(img, (0,0), fx=0.7, fy=0.7)
        cv2.imshow("img", show)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
        
        if plag is not None: # plag가 None이 아닌 것이 리턴된거면 is_accident이니 처리
            plag += int(over_threshold)*10
            if plag > 100: plag=100        
            if plag > 50:
                global MAX
                global is_on
                MAX = plag
                is_on = True
            
            if is_on:
                cnt+=1
                if cnt > 30:
                    cnt=0
                    is_on=False
                plag = MAX
                

            edge_data = receive_plag_data(plag, "Device1")  # Data.py를 통해 EdgeData로 변환
            sendDataToDataHub(edge_agent, edge_data)  # 변환된 EdgeData를 EdgeAgent.py를 통해 데이터 허브로 전송

       if video is not None:
           fourcc = cv2.VideoWriter_fourcc(*'mp4v')
           f = 30.0
           h, w, l = video[0][0].shape
           out = cv2.VideoWriter('output.mp4', fourcc, f, (w, h))
           for i in range(len(video)):
               out.write(video[i][0])
           out.release()
           os.system("python Stream.py &")
            
        ##### ---------- VISION ---------- #####
        #######################################

if __name__ == "__main__":
    main()
