import wx
import socket
import pyaudio
from threading import Thread
import sounddevice as sd

def startRecording():
    PORT = 12358

    p = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', PORT))
        print(f"Listening on {PORT}")
        while True:
            data, addr = s.recvfrom(65535)
            stream.write(data)

class Example(wx.Frame):
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)
        self.t = Thread(target=startRecording, daemon=True)
        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)
        startButton = wx.Button(pnl, label='Start', pos=(20, 40))
        startButton.Bind(wx.EVT_BUTTON, self.startThread)
        self.SetSize((350, 250))
        self.SetTitle('wx.Button')
        self.Centre()

    def startThread(self, e):
        self.t.start()

    def OnClose(self, e):
        self.Close(True)
        

def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()  