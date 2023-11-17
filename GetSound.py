import pyaudio
import numpy as np
import time

# Audio Stream Settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

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

# Read Audio Data
try:
    while True:
        current_time = time.time()

        if current_time - last_time >= 1:
            sound_level_average = np.mean(sound_level_list)
            print(f'Sound Level during 1sec: {sound_level_average}')
            sound_level_list = []
            last_time = current_time

        # Read audio stream data
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        
        # Calculate mean sound level
        sound_level = np.average(np.abs(data))
        sound_level_list.append(sound_level)

except KeyboardInterrupt:
    #Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Recording stopped")
