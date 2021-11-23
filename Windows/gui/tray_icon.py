import wx
import wx.adv
from constants import APP_NAME


# Class for the system tray icon of this app
class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame, icon):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame

        # Show micWindow on left click
        self.SetIcon(self.icon, APP_NAME)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.show_window)

        # Display options on right
        self.create_rclick_menu()
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.show_options)

    def create_rclick_menu(self):
        # Exit button, close program on click
        self.menu = wx.Menu()
        exit_button = self.menu.Append(wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.close_handler, exit_button)

    def close_handler(self, event):
        wx.Exit()

    def show_window(self, event):
        self.frame.Show()

    def show_options(self, event):
        self.PopupMenu(self.menu)