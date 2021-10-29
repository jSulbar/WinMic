import wx
import socket


# 
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


# A parent sizer class to hold other sizers.
class ParentSizer(wx.BoxSizer):
    def __init__(self, sizer = wx.HORIZONTAL) -> None:
        super().__init__(sizer)
        self.control_list = []

    def add_sizer(self, sizer, *args):
        if type(sizer) is not MySizer:
            raise TypeError('Argument is not an instance of MySizer')
        self.control_list.append(sizer)
        self.Add(sizer.sizer, *args)

    # Search inside this sizer for a control
    # with the given name
    def control_by_name(self, name):
        for sizer in self.control_list:
            for key in sizer.control_list:
                if key == name:
                    return sizer.control_list[name]

    # Bulk add sizers, all with the same args
    def add_sizers(self, proportion, flag, border, *sizers):
        for sizer in sizers:
            self.add_sizer(sizer, proportion, flag, border)


# After learning html it feels weird to put the UI design WITH
# the program... ah well.
class MicWindow(wx.Frame):
    def __init__(self, *args, **kw):
        # Make window unresizeable
        wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.v_sizer = ParentSizer(wx.VERTICAL)
        self.InitUI()

    def InitUI(self):
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
        h_sizer.add_control(ip_label, 'ip_label', 0, wx.ALIGN_CENTER | wx.ALL, 5)
        h_sizer2.add_control(start_button, 'start_button', 1, wx.ALIGN_BOTTOM | wx.ALL, 5)
        h_sizer2.add_control(stop_button, 'stop_button', 1, wx.ALIGN_BOTTOM | wx.ALL, 5)

        # Insert the rows into the column
        self.v_sizer.add_sizers(1, wx.EXPAND, 5, h_sizer, h_sizer2)

        # Insert the column into the panel
        self.v_sizer.SetSizeHints(pnl)
        pnl.SetSizer(self.v_sizer)

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