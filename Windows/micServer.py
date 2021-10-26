import wx
import socket
import pyaudio
from threading import Thread
import sounddevice as sd

class NetworkMic():
    def __init__(self, port, audioConfig):
        self.port = port
        self.config = audioConfig
        self.pyAudio = pyaudio.PyAudio()

    def startSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.port))

    def audioStream(self):
        stream = self.pyAudio.open(
            format=self.config["format"],
            channels=self.config["channels"],
            rate=self.config["rate"],
            output=True)
        return stream
    
    def startOutput(self):
        self.startSocket()
        stream = self.audioStream()
        while True:
            stream.write(self.socket.recv(65535))

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.mic = NetworkMic(12358, { "format":pyaudio.paInt16, "channels":1, "rate":44100 })
        self.t = Thread(target=self.mic.startOutput, daemon=True)
        self.InitUI()

    def InitUI(self):
        self.SetTitle('WinMic')
        self.SetSize((350, 250))
        self.Centre()
        self.addWidgets()
        
    def addWidgets(self):
        pnl = wx.Panel(self)
        startButton = wx.Button(pnl, label='Start', pos=(20, 40))
        startButton.Bind(wx.EVT_BUTTON, self.startThread)

    def startThread(self, e):
        self.t.start()

    def OnClose(self, e):
        self.Close(True)
        

def main():
    app = wx.App()
    ex = MyFrame(None)
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()  