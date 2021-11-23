"""
Module containing the underlying logic behind the GUI such as enabling/disabling buttons and
accessing the configuration file.
"""
import wx
import pyaudio

def parse_ctrls(ctrl_defs):
    """
    From a dictionary returned by ControlFactory, return a dictionary of controls
    formatted as { 'controlname': controlobject }.
    """
    ctrls_dict = {}
    for ctrl in ctrl_defs:
        if 'control' in ctrl:
            ctrls_dict[ctrl['name']] = ctrl['control']
        elif 'controls' in ctrl:
            for key in ctrl['controls']:
                ctrls_dict[key] = ctrl['controls'][key]
    return ctrls_dict

def bind_with_args(ctrl, evt_type, uses_event = False, *, callback, args):
    """
    Bind a wxPython control to a function specifying the arguments to be used by that function,
    instead of only having the event as a parameter. The "args" parameter should be a tuple containing
    the arguments to be passed to the callback provided.
    """
    if uses_event:
        ctrl.Bind(evt_type, lambda event: callback(event, *args))
    else:
        ctrl.Bind(evt_type, lambda event: callback(*args))


def skip_event(function):
    """
    Decorator for a wx event handler function, skips the event.
    Allowing for other bound functions to also be executed.
    """
    def func(self, event):
        function(self, event)
        event.Skip()
    return func


class MainWindowBackend:
    def __init__(self, mic_player, socket, minimize):
        self.mic_player = mic_player
        self.socket = socket
        self.to_tray_onclose = minimize

    def inject_controls(self, ctrls_list):
        """
        Injects the controls created by ControlFactory into this object,
        forming part of its instance.
        """
        ctrls_list = parse_ctrls(ctrls_list)
        self.iplabel = ctrls_list['ip_label']
        self.device_select = ctrls_list['device_select']
        self.startbtn = ctrls_list['start_button']
        self.stopbtn = ctrls_list['stop_button']

    def bind_controls(self):
        self.startbtn.Bind(wx.EVT_BUTTON, self.micbtns_toggle)
        self.startbtn.Bind(wx.EVT_BUTTON, self.start_mic)

        self.stopbtn.Bind(wx.EVT_BUTTON, self.micbtns_toggle)
        self.stopbtn.Bind(wx.EVT_BUTTON, self.stop_mic)

    @skip_event
    def micbtns_toggle(self, event):
        """
        Toggles start and stop microphone buttons.
        """
        # If we can disable start button, we know
        # stop button is disabled and viceversa.
        if self.startbtn.Disable():
            self.stopbtn.Enable()
        elif self.stopbtn.Disable():
            self.startbtn.Enable()

    @skip_event
    def start_mic(self, event):
        self.mic_player.start(self.socket)

    @skip_event
    def stop_mic(self, event):
        self.mic_player.stop()

    def bind_mainwindow_close(self, frame):
        frame.Bind(wx.EVT_CLOSE, self.mainwindow_close)

    def mainwindow_close(self, event):
        if self.to_tray_onclose is True:
            event.GetEventObject().Hide()
        else:
            wx.Exit()