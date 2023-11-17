import ffmpeg, os

def stream_accident():
    os.system("ffmpeg -i output.mp4 -f lavfi -i anullsrc -c:v copy -c:a aac -shortest audio.mp4")
    
    input_video = './audio.mp4'
    
    stream_url = 'rtmp://a.rtmp.youtube.com/live2'
    stream_key = '6a3r-0zzr-gbt4-53ur-045x'  # YouTube에서 제공하는 스트림 키
    
    # ffmpeg 스트림 설정
    
    stream = (
        ffmpeg
        .input(input_video, stream_loop=1)
        .output(stream_url + '/' + stream_key, format='flv', vcodec='libx264', r='30', pix_fmt='yuv420p')
        .run_async(pipe_stdin=True)
    )
    
    # 스트리밍 진행
    try:
        stream.communicate()
    except KeyboardInterrupt:
        stream.kill()


    os.system("rm -rf audio.mp4")


if __name__=="__main__":
    stream_accident()