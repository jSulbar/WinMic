import socket
import wx
import pyaudio
from threading import Thread


# Class for microphone IO.
class MicInstance:
    def __init__(self) -> None:
        self.running = False

    # Writes data to VBCable input
    def thread_target(self, stream, socket):
        while self.running:
            audio_data = socket.receive_buffer()
            stream.write(audio_data)

    # Sets the running flag to false,
    # stopping the thread
    def stop(self):
        self.running = False

    # Starts the thread with the given socket.
    def start(self, stream, socket):
        self.running = True
        thread = Thread(target=self.thread_target,
                        args=(stream, socket),
                        daemon=True)
        thread.start()

# I don't know if this class' existence is necessary but w/e
# Manage UDP socket
class DatagramSocket:
    def __init__(self, port) -> None:
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind_socket(self, addr = ''):
        self.socket.bind((addr, self.port))

    # Receive audio from phone
    def receive_buffer(self, bufsize = 32768):
        return self.socket.recv(bufsize)

    # Really hackish way of getting local ip.
    # https://stackoverflow.com/questions/166506/
    def get_local_ip(self = None):
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(('8.8.8.8', 1))
        return temp_socket.getsockname()[0]


# Class that connects the UI with the socket
# and audio stream.
class MicManager:
    def __init__(self, frame) -> None:
        self.mic_instance = MicInstance()
        self.frame = frame

    # Set up UI elements
    def setup(self):
        # Add ip address to label
        ip_control = self.frame.control_by_name('ip_label')
        ip_control.LabelText += DatagramSocket.get_local_ip()

        # Bind start and stop buttons to the mic object
        start_button = self.frame.control_by_name('start_button')
        stop_button = self.frame.control_by_name('stop_button')
        start_button.Bind(wx.EVT_BUTTON, self.start_mic)
        stop_button.Bind(wx.EVT_BUTTON, self.stop_mic)

    # Start/stop methods for mic. 
    # For now, settings are hardcoded in.
    def start_mic(self, event):
        self.frame.toggle_buttons()

        pa = pyaudio.PyAudio()
        stream = pa.open(44100, 1, pyaudio.paInt16, output=True)
        socket = DatagramSocket(12358)
        socket.bind_socket()

        self.mic_instance.start(stream, socket)

    def stop_mic(self, event):
        self.frame.toggle_buttons()
        self.mic_instance.stop()