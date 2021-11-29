"""
Module containing the underlying logic behind the GUI such as enabling/disabling buttons and
accessing the configuration file.
"""
import wx
import pyaudio
from constants import CFGKEY_TRAY, CFGKEY_LANGUAGE, AVAILABLE_LANGS, HOST_APIS, CFGKEY_HOSTAPI


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


class OptionsController:
    """
    Contains the code for changing the app configuration that is needed by
    the OptionsMenu.
    """
    def __init__(self, option_menu, cfg):
        self.menu = option_menu
        self.cfg = cfg

    def bind_controls(self):
        self.menu.Bind(wx.EVT_MENU, self._traycfg_event, self.menu.minimize_to_tray)
        self._cfgwrite_bindings(self.menu.langmenu_items, CFGKEY_LANGUAGE, AVAILABLE_LANGS)
        self._cfgwrite_bindings(self.menu.apimenu_items, CFGKEY_HOSTAPI, HOST_APIS)

    def _cfgwrite_bindings(self, submenu_items, cfgkey, submenu_dict):
        """
        Write bindings for a submenu to save its changes to the config file.
        """
        for item in submenu_items:
            def callback(event, item=item):
                self.cfg.Write(cfgkey, str(submenu_dict[item]))
                self.cfg.Flush()
                event.Skip()
            self.menu.Bind(wx.EVT_MENU, callback, submenu_items[item])

    @skip_event
    def _traycfg_event(self, event):
        """
        Write to config when minimize to tray option is checked or unchecked.
        """
        checked = self.menu.minimize_to_tray.IsChecked()
        self.cfg.Write(CFGKEY_TRAY, str(checked))
        self.cfg.Flush()


class MainWindowBackend:
    def __init__(self, mic_player, socket, cfg):
        self.mic_player = mic_player
        self.socket = socket
        self.cfg = cfg
        self.audio_devices = {}

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

    def fill_control_data(self):
        """
        Gives informational controls inside this window the data they 
        need to display, like the local IP inside the ip label, which
        is provided by the socket.
        """
        # Set IP on label
        self.iplabel.LabelText += self.socket.get_local_ip()

        # Populate audio device selection
        for i in range(self.mic_player.get_device_count()):
            device = self.mic_player.get_device_info_by_index(i)
            if device['hostApi'] == self.cfg.get_host_api() and device['maxOutputChannels'] > 0:
                self.audio_devices[device['name']] = device['index']
                self.device_select.Append(device['name'])
        
        # Start with the first device already selected
        self.device_select.SetSelection(0)

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
        if self.audio_devices:
            # Get the selected audio device
            choice_index = self.device_select.GetCurrentSelection()
            selected_device = self.device_select.GetString(choice_index)

            # Start streaming to it
            self.mic_player.start(self.socket, self.audio_devices[selected_device])
        else:
            # Else just use the default device PyAudio picks
            self.mic_player.start(self.socket)

    @skip_event
    def stop_mic(self, event):
        self.mic_player.stop()

    def bind_mainwindow_close(self, frame, tray_icon):
        frame.Bind(wx.EVT_CLOSE, self.mainwindow_close(tray_icon))

    def mainwindow_close(self, tray_icon):
        """
        Returns the event handler for the application's close.
        """
        def handler(event):
            mainwindow = event.GetEventObject()
            if self.cfg.get_tray_cfg() is True:
                mainwindow.Hide()
            else:
                tray_icon.Destroy()
                mainwindow.Destroy()
        return handler