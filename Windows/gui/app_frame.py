import wx
from .tray_icon import TrayIcon
from .nested_sizer import ParentSizer
    
        
class MicWindow(wx.Frame):
    def __init__(self):
        # Make window unresizeable
        wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.sizer = ParentSizer(wx.VERTICAL)

        # System tray icon
        self.tray_icon = TrayIcon(self)

        # Locale object for multi-language support
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)

        # Bind close buttons to handler
        self.Bind(wx.EVT_CLOSE, self.close_handler)

        # Folder and filename for translations
        wx.Locale.AddCatalogLookupPathPrefix('locale')
        self.locale.AddCatalog('i18n')

    def init_gui(self):
        # Set window title and center
        self.SetTitle('WinMic')
        self.SetSize(((320, 160)))
        self.Centre()

    # Hide or close window depending on user input
    def close_handler(self, event):
        hide_onclose = self.sizer.control_by_name('tray_checkbox').GetValue()
        if hide_onclose:
            self.Hide()
        else:
            self.tray_icon.Destroy()
            self.Destroy()

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
        label=_('Your IPv4 address is: '))

        # Give user the option to send app to tray
        tray_checkbox = wx.CheckBox(pnl,
        label=_('Hide to tray on window close'))

        self.sizer.new_control(ip_label, 'ip_label', 
        control_options=(0, wx.ALIGN_CENTER | wx.ALL, 5),
        sizer_options=(0, wx.ALL | wx.ALIGN_CENTER, 5))

        self.sizer.new_control(tray_checkbox, 'tray_checkbox',
        control_options=(0, wx.ALIGN_LEFT | wx.ALL, 5),
        sizer_options=(1, wx.ALL | wx.ALIGN_LEFT, 5))

        self.sizer.new_controls_row({ 
            "start_button":start_button,
            "stop_button":stop_button
        }, control_options=(1, wx.ALIGN_BOTTOM | wx.ALL, 5),
        sizer_options=(1, wx.EXPAND, 5))

        # Bind sizer to panel
        self.sizer.SetSizeHints(pnl)
        pnl.SetSizer(self.sizer)