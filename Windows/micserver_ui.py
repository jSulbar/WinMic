import wx
import locale


# Custom sizer to help manage and search for elements
class ChildSizer(wx.BoxSizer):
    def __init__(self, sizer = wx.HORIZONTAL) -> None:
        super().__init__(sizer)
        # Dict with every control that has been added
        # To this sizer
        self.control_list = {}

    # Adds control to list, then to wx.boxsizer instance
    def add_control(self, control, name, *args):
        if name in self.control_list.keys():
            raise Exception('A control with the given name already exists')
        self.control_list[name] = control
        self.Add(control, *args)

    # Returns the control with the given name
    def get_control(self, name):
        return self.control_list[name]


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


class MicWindow(wx.Frame):
    def __init__(self):
        # Make window unresizeable
        wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.sizer = ParentSizer(wx.VERTICAL)

        # Locale object for multi-language support
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)

        # Set translation folder and filenames
        wx.Locale.AddCatalogLookupPathPrefix('locale')
        self.locale.AddCatalog('i18n')

    def init_gui(self):
        # Set window title and center
        self.SetTitle('WinMic')
        self.Centre()

    # Shorthand function 
    # so i don't have to write micwindow.sizer.control_by_name
    def control_by_name(self, name):
        return self.sizer.control_by_name(name)

    def toggle_buttons(self):
        # Get buttons by name
        start_button = self.sizer.control_by_name('start_button')
        stop_button = self.sizer.control_by_name('stop_button')

        # Toggle start/stop buttons
        if start_button.Disable():
            stop_button.Enable()
        elif stop_button.Disable():
            start_button.Enable()

    # Bind a control to an event
    def bind_control(self, name, event, callback):
        control = self.sizer.control_by_name(name)
        control.Bind(event, callback)
        
    # Function to add controls to window
    def add_controls(self):
        # Create a panel container to put controls in
        pnl = wx.Panel(self)

        # Needs to be an underscore for gettext to parse it.
        _ = wx.GetTranslation

        # Create stop/start buttons for mic
        # stop button is initially disabled
        start_button = wx.Button(pnl, label=_('Start recording'))
        stop_button = wx.Button(pnl, label=_('Stop recording'))
        stop_button.Disable()

        # Make a label that will display
        # the pc's IPv4 address
        ip_label = wx.StaticText(pnl, 
        label=_('Your IPv4 address is '))

        self.sizer.new_control(ip_label, 'ip_label', 
        control_options=(0, wx.ALIGN_CENTER | wx.ALL, 5),
        sizer_options=(1, wx.ALL, 5))

        self.sizer.new_controls_row({ 
            "start_button":start_button,
            "stop_button":stop_button
        }, control_options=(1, wx.ALIGN_BOTTOM | wx.ALL, 5),
        sizer_options=(1, wx.EXPAND, 5))

        # Bind sizer to panel
        self.sizer.SetSizeHints(pnl)
        pnl.SetSizer(self.sizer)