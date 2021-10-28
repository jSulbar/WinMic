import wx
import socket
import pyaudio
from wx.core import Sizer

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



# Class to not make this so insufferable
class MySizer:
    def __init__(self, sizer = wx.HORIZONTAL) -> None:
        self.sizer = wx.BoxSizer(sizer)
        self.control_list = {}

    def add_control(self, widget, name, *args):
        self.control_list[name] = widget
        self.sizer.Add(widget, *args)

    def get_control(self, name):
        return self.control_list[name]

    def add_sizer(self, sizer, name):
        self.control_list[name] = sizer


class ParentSizer:
    def __init__(self, sizer = wx.HORIZONTAL) -> None:
        self.sizer = wx.BoxSizer(sizer)
        self.control_list = []

    def add_sizer(self, sizer):
        if type(sizer) is not MySizer:
            raise TypeError('Argument is not an instance of MySizer')
        self.control_list.append(sizer)
        self.sizer.Add(sizer.sizer, 1, wx.EXPAND, 5) # Hardcoded args for now

    def control_by_name(self, name):
        for sizer in self.control_list:
            for key in sizer.control_list:
                if key == name:
                    return sizer.control_list[name]

    def add_sizers(self, *sizers):
        for sizer in sizers:
            self.add_sizer(sizer)


# After learning html it feels weird to put the UI design WITH
# the program... ah well.
class MicWindow(wx.Frame):
    def __init__(self, *args, **kw):
        # This method of making the window unresizable brought to you by wxpython docs
        # https://wxpython.org/Phoenix/docs/html/wx.Frame.html
        wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.v_sizer = ParentSizer(wx.VERTICAL)
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
        h_sizer = MySizer(wx.HORIZONTAL)
        h_sizer2 = MySizer(wx.HORIZONTAL)

        # Create stop/start buttons for mic
        # stop button is initially disabled
        start_button = wx.Button(pnl, label='Start mic')
        stop_button = wx.Button(pnl, label='Stop mic')
        stop_button.Disable()

        # Make a label displaying this pc's ipv4 address
        ip_addr = socket.gethostbyname(socket.gethostname())
        ip_label = wx.StaticText(pnl, 
        label=f"Your IPv4 address: {ip_addr}")

        # add function to a button when it's clicked
        start_button.Bind(wx.EVT_BUTTON, self.start_mic)
        stop_button.Bind(wx.EVT_BUTTON, self.stop_mic)

        # Add ip label to first row, stop/start buttons to second
        # Give all elements a border of 5 pixels
        h_sizer.add_control(ip_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        h_sizer2.add_control(start_button, 'start_button', 1, wx.ALIGN_BOTTOM | wx.ALL, 5)
        h_sizer2.add_control(stop_button, 'stop_button', 1, wx.ALIGN_BOTTOM | wx.ALL, 5)

        # Insert the rows into the column
        self.v_sizer.add_sizers(h_sizer, h_sizer2)

        # Insert the column into the panel
        # This looks fugly
        self.v_sizer.sizer.SetSizeHints(pnl)
        pnl.SetSizer(self.v_sizer.sizer)

    def start_mic(self, e):
        start_button = e.GetEventObject()
        stop_button = self.v_sizer.control_by_name('stop_button')

        start_button.Disable()
        stop_button.Enable()

    def stop_mic(self, e):
        stop_button = e.GetEventObject()
        start_button = self.v_sizer.control_by_name('start_button')

        start_button.Enable()
        stop_button.Disable()


def main():
    app = wx.App()
    ex = MicWindow()
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()