import boto3
import cv2
from config import *

folder_path = './BE/Accident'
    
bucket = 'son-hyunho-icn-reviewweb-bucket'
s3_filename = 'cctv.jpg'
s3_videoname = 'accident.mp4'
image_key = f'videos/{s3_filename}'
video_key = f'videos/{s3_videoname}'
image_url = f'https://{bucket}.s3.amazonaws.com/{image_key}'

# AWS 서비스에 연결
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

s3 = session.resource('s3')
s3_obj = s3.Object(bucket, image_key)
s3_obj2 = s3.Object(bucket, video_key)

def resize_image(file):
    res = cv2.resize(file, dsize=(600, 400), interpolation=cv2.INTER_CUBIC)
    image_bytes = cv2.imencode('.jpg', res)[1].tobytes()
    return image_bytes

def upload_mp4(file_name):
    file = cv2.imread(file_name)
    image_bytes = resize_image(file)
    s3_obj.put(Body = image_bytes, ContentType='image/jpeg')
    print(image_url)                
    
def upload_image(file):
    image_bytes = resize_image(file)
    s3_obj.put(Body = image_bytes, ContentType='image/jpeg')
    print(image_url)    
    

def resize_video(input_file_path, output_file_path, width=600, height=400):
    cap = cv2.VideoCapture(input_file_path)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))
    
    # 동영상의 각 프레임을 리사이즈하고 저장
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
        out.write(resized_frame)
    
    # 모든 작업을 마치고 자원을 해
    cap.release()
    out.release()

def upload_mp4(file_name, bucket_name=bucket, object_name='re.mp4'):
    
    with open(file_name, 'rb') as data:
        s3_obj2.put(Body=data, ContentType='video/mp4')
    
    image_url = f"https://{bucket_name}.s3.amazonaws.com/{video_key}"
    print(image_url)