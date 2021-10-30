import wx
import threading
import pyaudio
from micserver import DatagramSocket
from micserver_ui import MicWindow

class MicInstance:
    def __init__(self, stream, socket) -> None:
        self.running = False
        self.stream = stream
        self.socket = socket
        self.toggle = None

    def thread_target(self, stream, socket):
        self.running = True
        if self.running:
            data = socket.receive_buffer()
            stream.write(data)

    def stop(self, e):
        self.toggle()

        self.running = False

    def set_toggle(self, callback):
        self.toggle = callback

    def start(self, e):
        self.toggle()

        thread = threading.Thread(target=self.thread_target, 
        args=(self.stream, self.socket), daemon=True)
        thread.start()


def main():
    app = wx.App()

    socket = DatagramSocket(12358)
    socket.bind_socket()
    pa = pyaudio.PyAudio()
    stream = pa.open(44100, 1, pyaudio.paInt16, output=True)

    mic = MicInstance(stream, socket)
    
    # Create micwindow 
    ex = MicWindow()
    # Set IP to show in window
    ex.set_ip(socket.get_local_ip())
    ex.init_gui()

    ex.bind_control('start_button', wx.EVT_BUTTON, mic.start)
    ex.bind_control('stop_button', wx.EVT_BUTTON, mic.stop)

    mic.set_toggle(ex.toggle_buttons)

    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()