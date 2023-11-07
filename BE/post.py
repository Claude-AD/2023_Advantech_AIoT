import boto3
from botocore.exceptions import NoCredentialsError
import os
import time
import cv2

folder_path = './BE/Accident'
    
bucket = 'son-hyunho-icn-reviewweb-bucket'
s3_filename = 'cctv'
image_key = f'videos/{s3_filename}'
image_url = f'https://{bucket}.s3.amazonaws.com/{image_key}'

session = boto3.Session()
s3 = session.resource('s3')
s3_obj = s3.Object(bucket, image_key)

def resize_image(file):
    img = cv2.imread(file)
    res = cv2.resize(img, dsize=(600, 400), interpolation=cv2.INTER_CUBIC)
    image_bytes = cv2.imencode('.jpg', res)[1].tobytes()
    return image_bytes

def upload_image(file):
    image_bytes = resize_image(file)
    s3_obj.put(Body = image_bytes, ContentType='image/jpeg')
    print(image_url)

if __name__ == '__main__':
    while(True):
        for filename in os.listdir(folder_path):
            if filename.endswith('.jpg'):
                file = os.path.join(folder_path, filename)
                upload_image(file)
                time.sleep(1)
                