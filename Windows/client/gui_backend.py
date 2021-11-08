import wx
import pyaudio
from .udp_socket import DatagramSocket
from .mic_player import MicPlayer


# Class that connects the UI with the socket
# and audio stream.
class BackendConnector:
    def __init__(self, frame, app) -> None:
        self.frame = frame
        self.app = app

    # Set up UI elements
    def setup(self):
        # Set window title
        self.frame.SetTitle(self.app.AppName)

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

        self.mic_instance = MicPlayer(stream, socket)
        self.mic_instance.start()

    def stop_mic(self, event):
        self.frame.toggle_buttons()
        self.mic_instance.stop()