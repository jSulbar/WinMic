import wx
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
        

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        # This method of making the window unresizable brought to you by wxpython docs
        # https://wxpython.org/Phoenix/docs/html/wx.Frame.html
        wx.Frame.__init__(self, None, 
        style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.InitUI()

    def InitUI(self):
        size = (320, 120)
        self.SetSize(size)

        # Set window title and center
        self.SetTitle('WinMic')
        self.Centre()

        # Add controls to frame
        self.addWidgets()
        
    # Function to add controls to window
    def addWidgets(self):
        # Create a panel container to put controls in
        pnl = wx.Panel(self)

        # Create grid for UI (or closest thing anyway)
        # 1 column, 2 rows
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # Get the ipv4 address of this PC
        ip_addr = socket.gethostbyname(socket.gethostname())

        # Create stop/start buttons for mic
        start_button = wx.Button(pnl, label='Start mic', id=1)
        stop_button = wx.Button(pnl, label='Stop mic', id=2)
        stop_button.Disable()

        # add function to a button when it's clicked
        start_button.Bind(wx.EVT_BUTTON, self.start_mic)
        stop_button.Bind(wx.EVT_BUTTON, self.start_mic)

        # Make a label displaying this pc's ip
        ip_label = wx.StaticText(pnl, label=f"Your IPv4 address: {ip_addr}")

        # Add ip label to first row, stop/start buttons to second
        # Give all elements a border of 5 pixels
        h_sizer.Add(ip_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        h_sizer2.Add(start_button, 1, wx.ALIGN_BOTTOM | wx.ALL, 5)
        h_sizer2.Add(stop_button, 1, wx.ALIGN_BOTTOM | wx.ALL, 5)

        # Insert the rows into the column
        v_sizer.Add(h_sizer, 1, wx.EXPAND, 5)
        v_sizer.Add(h_sizer2, 1, wx.EXPAND, 5)

        # Insert the column into the panel
        v_sizer.SetSizeHints(pnl)
        pnl.SetSizer(v_sizer)

    def start_mic(self, e):
        d = e.GetEventObject()
        d.Disable()
    def stop_mic(self, e):
        pass


def main():
    app = wx.App()
    ex = MyFrame()
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()