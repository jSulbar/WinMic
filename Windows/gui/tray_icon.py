import wx
import wx.adv
from constants import APP_NAME


# Class for the system tray icon of this app
class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame, icon):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame

        # Show main window on left click
        self.SetIcon(icon, APP_NAME)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, lambda e: self.frame.Show())

        # Display options on right
        self.create_rclick_menu()
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, lambda e: self.PopupMenu(self.menu))

        self.bind_close_handler()

    def create_rclick_menu(self):
        # Exit button, close program on click
        self.menu = wx.Menu()
        self.exit_button = self.menu.Append(wx.ID_EXIT)

    def bind_close_handler(self):
        def close(event):
            self.frame.Destroy()
            self.Destroy()
        self.menu.Bind(wx.EVT_MENU, close, self.exit_button)