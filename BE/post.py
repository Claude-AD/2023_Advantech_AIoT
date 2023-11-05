import boto3
from botocore.exceptions import NoCredentialsError
import os
import time
import cv2

def upload_image(file, bucket, s3_file):
    img = cv2.imread(file)
    res = cv2.resize(img, dsize=(400, 300), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('resized_image.jpg', res)
    resized_image = './resized_image.jpg'
    with open(resized_image, 'rb') as file_data:
        image_key = f'videos/{s3_file}'
        s3_obj = s3.Object(bucket, image_key)
        s3_obj.put(Body = file_data, ContentType='image/jpeg')
    image_url = f'https://{bucket}.s3.amazonaws.com/{image_key}'
    print(image_url)
    time.sleep(1)

if __name__ == '__main__':
    folder_path = '../BE/data'
    
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket_name = 'son-hyunho-icn-reviewweb-bucket'
    s3_file = 'cctv'
    
    while(True):
        for filename in os.listdir(folder_path):
            if filename.endswith('.jpg'):
                file = os.path.join(folder_path, filename)
                upload_image(file, bucket_name, s3_file)
                