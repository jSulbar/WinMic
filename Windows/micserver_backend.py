import socket
import wx
import pyaudio
from threading import Thread


# Class for microphone IO.
class MicInstance:
    def __init__(self, stream, socket) -> None:
        self.running = False
        self.stream = stream
        self.socket = socket

    # Writes data to VBCable input
    def thread_target(self):
        while self.running:
            audio_data = self.socket.recv(self.socket.bufsize)
            self.stream.write(audio_data)
        self.stream.close()
        self.socket.close()

    # Sets the running flag to false,
    # stopping the thread
    def stop(self):
        self.running = False

    # Starts the thread with the given socket.
    def start(self):
        self.running = True
        thread = Thread(target=self.thread_target,
                        daemon=True)
        thread.start()


# UDP socket class
class DatagramSocket(socket.socket):
    def __init__(self, port, bufsize = 32768) -> None:
        # Init as UDP using local network
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)

        # Make socket reusable to disable TIME_WAIT between sockets
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
        self.bufsize = bufsize

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
        socket.bind(('', socket.port))

        self.mic_instance = MicInstance(stream, socket)
        self.mic_instance.start()

    def stop_mic(self, event):
        self.frame.toggle_buttons()
        self.mic_instance.stop()