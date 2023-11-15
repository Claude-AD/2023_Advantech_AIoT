from Vision import process_frame
from datahub.Data import receive_plag_data
from datahub.EdgeAgent import generate_edgeAgent, sendDataToDataHub
import cv2, time
from post import upload_image, upload_mp4

def main():
    edge_agent = generate_edgeAgent()  # EdgeAgent 인스턴스 생성 및 설정
    fps = 0
    while True:
        img, plag, fps, video = process_frame(fps)  # img와 plag 혹은 img와 None을 받음

        if img is None and plag is None: # img, plag 둘 다 None이면 영상이 끝난것이니 종료
            print("No more frames to process or unable to open video. Exiting.")
            break
        elif img is 0: # 1초가 지나지 않았을 때
            pass
        else:          # 1초(30프레임)마다 사진 보내기
            upload_image(img)   #'''img 보내기'''
            
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
            time.sleep(5)   # 5초간 기다리기

if __name__ == "__main__":
    main()
