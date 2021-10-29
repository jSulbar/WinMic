import socket
import pyaudio


class AudioStream:
    def __init__(self, **kwargs) -> None:
        self.format = kwargs['format']
        self.channels = kwargs['channels']
        self.sample_rate = kwargs['sample_rate']
        self.pa_stream = None

    def open_stream(self):
        pa = pyaudio.PyAudio()
        self.pa_stream = pa.open(self.sample_rate, self.channels, self.format, output=True)

    def stream_write(self, data):
        self.pa_stream.write(data)


class DatagramSocket:
    def __init__(self, port) -> None:
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind_socket(self, addr = ''):
        self.socket.bind((addr, self.port))

    def receive_buffer(self, bufsize = 32768):
        return self.socket.recv(bufsize)


class NetworkMic(DatagramSocket, AudioStream):
    def __init__(self, port) -> None:
        super(DatagramSocket).__init__(port)
