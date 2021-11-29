import wx

from gui.layout_definitions import MAIN_WINDOW_LAYOUT
from gui.nested_sizer import ParentSizer
from gui.tray_icon import TrayIcon
from gui.control_factory import ControlFactory
from gui.menus import OptionsMenu

from client.config_file import WinMicConfig
from client.gui_backend import MainWindowBackend, OptionsController
from client.udp_socket import DatagramSocket
from client.mic_player import MicPlayer
from client.winmic_app import WinMicApp

from constants import APP_NAME, DEFAULT_APP_CONFIG, DEFAULT_PORT, CFG_FILENAME
from winmic_icon import winmic_icon

_ = wx.GetTranslation

if __name__ == '__main__':

    # Init wxPython app
    app = WinMicApp()
    appicon = wx.Icon(winmic_icon.GetIcon())

    # Make unresizable window, set title
    window = wx.Frame(None, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
    window.SetTitle(APP_NAME)
    window.SetIcon(appicon)
    window.Center()

    # Read language from config and set it
    cfg = WinMicConfig(APP_NAME, CFG_FILENAME, DEFAULT_APP_CONFIG)
    lang = cfg.get_language()
    app.set_lang(lang)

    # Create boxsizer and control container for main window
    micframe_sizer = ParentSizer()
    panel = wx.Panel(window)

    # Create controls for main window and add them to its sizer
    factory = ControlFactory(panel)
    controls = factory.get_controls(MAIN_WINDOW_LAYOUT)
    micframe_sizer.controls_from_factory(controls)

    tray_enabled = cfg.get_tray_cfg()
    host_api = cfg.get_host_api()

    # Create menu bar, add settings menu to it
    menu_bar = wx.MenuBar()
    options_menu = OptionsMenu(tray_enabled, lang, host_api)
    menu_bar.Append(options_menu, _('Options'))

    window.SetMenuBar(menu_bar)

    # Lock the sizer onto the main window
    micframe_sizer.SetSizeHints(panel)
    window.SetSizerAndFit(micframe_sizer)

    # Create tray icon for the app
    tray = TrayIcon(window, appicon)

    # Init socket and micplayer
    sock = DatagramSocket(DEFAULT_PORT)
    sock.bind(('', sock.port))
    micplayer = MicPlayer()

    # Start main window's "business logic" class
    window_backend = MainWindowBackend(micplayer, sock, cfg)
    window_backend.inject_controls(controls)
    window_backend.fill_control_data()

    # Bind main window's GUI to underlying logic
    window_backend.bind_controls()
    window_backend.bind_mainwindow_close(window, tray)
    options_backend = OptionsController(options_menu, cfg)
    options_backend.bind_controls()

    window.Show()
    app.MainLoop()