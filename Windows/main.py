import wx
from gui.app_frame import MicWindow
from micserver_backend import MicManager


if __name__ == '__main__':

    # Start wxPython app
    app = wx.App()
    
    # Init window and add controls
    ex = MicWindow()
    ex.init_gui()
    ex.add_controls()

    backend = MicManager(ex)
    backend.setup()

    ex.Show()
    app.MainLoop()