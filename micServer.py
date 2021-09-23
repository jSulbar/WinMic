import socket
import pyaudio
import sounddevice as sd
PORT = 12358

p = pyaudio.PyAudio()
CHUNK = 65535
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('', PORT))
    print(f"Listening on {PORT}")
    while True:
        data, addr = s.recvfrom(65535)
        stream.write(data)