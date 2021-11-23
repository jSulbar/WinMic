import wx

from gui.layout_definitions import MAIN_WINDOW_LAYOUT
from gui.nested_sizer import ParentSizer
from gui.tray_icon import TrayIcon
from gui.control_factory import ControlFactory

from client.config_file import WinMicConfig
from client.gui_backend import MainWindowBackend
from client.udp_socket import DatagramSocket
from client.mic_player import MicPlayer
from client.winmic_app import WinMicApp

from constants import APP_NAME, DEFAULT_APP_CONFIG, DEFAULT_PORT, CFG_FILENAME


def parse_ctrls(ctrl_defs):
        ctrls_dict = {}
        for ctrl in ctrl_defs:
            if 'control' in ctrl:
                ctrls_dict[ctrl['name']] = ctrl['control']
            elif 'controls' in ctrl:
                for key in ctrl['controls']:
                    ctrls_dict[key] = ctrl['controls'][key]
        return ctrls_dict


if __name__ == '__main__':

    app = WinMicApp()

    # Make unresizable window, set title
    window = wx.Frame(None, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
    window.SetTitle(APP_NAME)
    window.Center()

    # Read language from config and set it
    cfg = WinMicConfig(APP_NAME, CFG_FILENAME, DEFAULT_APP_CONFIG)
    lang = int(cfg.Read('language'))
    app.set_lang(lang)

    micframe_sizer = ParentSizer()
    panel = wx.Panel(window)

    # Create controls for main window and add to sizer
    factory = ControlFactory(panel)
    controls = factory.get_controls(MAIN_WINDOW_LAYOUT)
    micframe_sizer.controls_from_factory(controls)
    parsedctrls = parse_ctrls(controls)

    #TODO: fix duct tape
    parsedctrls['ip_label'].LabelText += DatagramSocket.get_local_ip()

    sock = DatagramSocket(DEFAULT_PORT)
    sock.bind(('', sock.port))
    micplayer = MicPlayer()

    # Read from config if the window should be sent to tray or closed.
    # TODO: fix also this duct tape
    tray_cfg = cfg.Read('minimize_to_tray') == 'True'
    window_backend = MainWindowBackend(micplayer, sock, tray_cfg)
    window_backend.inject_controls(parsedctrls)

    window_backend.bind_controls()
    window_backend.bind_mainwindow_close(window)

    tray = TrayIcon(window)

    micframe_sizer.SetSizeHints(panel)
    window.SetSizerAndFit(micframe_sizer)

    window.Show()
    app.MainLoop()