import wx
import socket


# Custom sizer to help manage and search for elements
class ChildSizer(wx.BoxSizer):
    def __init__(self, sizer = wx.HORIZONTAL) -> None:
        super().__init__(sizer)
        # Dict with every control that has been added
        # To this sizer
        self.sizer_list = {}

    # Adds control to list, then to wx.boxsizer instance
    def add_control(self, control, name, *args):
        self.sizer_list[name] = control
        self.Add(control, *args)

    # Returns the control with the given name
    def get_control(self, name):
        return self.sizer_list[name]


# A parent sizer class to hold other sizers,
# and to make it less repetitive to add controls
class ParentSizer(wx.BoxSizer):
    def __init__(self, sizer = wx.HORIZONTAL) -> None:
        super().__init__(sizer)
        # List of child sizers to keep track of
        self.sizer_list = []

    # Add child to this sizer
    def add_sizer(self, sizer, *args):
        # Only accept ChildSizers
        if type(sizer) is not ChildSizer:
            raise TypeError('Argument is not an instance of ChildSizer')

        # Add to list
        self.sizer_list.append(sizer)
        self.Add(sizer, *args)

    # Search inside child sizers for a control
    # with the given name
    def control_by_name(self, name):
        for childsizer in self.sizer_list:
            for key in childsizer.control_list:
                if key == name:
                    return childsizer.control_list[name]

    # Create empty sizers in bulk
    def bulk_add_sizers(self, proportion, flag, border, *sizers):
        for sizer in sizers:
            self.add_sizer(sizer, proportion, flag, border)

    # Add a new control
    def new_control(self, control, name, *, sizer_options, control_options):
        if isinstance(control, wx.Control):
            # Create a new sizer for it
            new_sizer = ChildSizer(wx.HORIZONTAL)
            new_sizer.add_control(control, name, *control_options)

            self.add_sizer(new_sizer, *sizer_options)
        else:
            raise TypeError('Argument must be a wxWidgets control!')

    # Add multiple controls and put them inside a single sizer
    # Takes a dict formatted as { "controlname":control }
    def new_controls_row(self, controls, *, sizer_options, control_options):
        if type(controls) is dict:
            new_sizer = ChildSizer(wx.HORIZONTAL)

            for key in controls:
                new_sizer.add_control(controls[key], key, *control_options)

            self.add_sizer(new_sizer, *sizer_options)
        else:
            raise TypeError('Argument must be dict in the format { "controlname":control }')


# After learning html it feels weird to put the UI design WITH
# the program... ah well.
class MicWindow(wx.Frame):
    def __init__(self, *args, **kw):
        # Make window unresizeable
        wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.sizer = ParentSizer(wx.VERTICAL)
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

        # Create stop/start buttons for mic
        # stop button is initially disabled
        start_button = wx.Button(pnl, label='Start mic')
        stop_button = wx.Button(pnl, label='Stop mic')
        stop_button.Disable()

        # Make a label displaying this pc's ipv4 address
        ip_label = wx.StaticText(pnl, 
        label="Your IPv4 address: [address goes here]")

        self.sizer.add_control(ip_label, 'ip_label', 
        control_options=(0, wx.ALIGN_CENTER | wx.ALL, 5),
        sizer_options=(1, wx.ALL, 5))

        self.sizer.add_controls({ 
            "start_button":start_button,
            "stop_button":stop_button
        }, control_options=(1, wx.ALIGN_BOTTOM | wx.ALL, 5),
        sizer_options=(1, wx.EXPAND, 5))

        # Bind sizer to panel
        self.sizer.SetSizeHints(pnl)
        pnl.SetSizer(self.sizer)