import wx
from gui.app_frame import MicFrame
from micserver_backend import MicManager


if __name__ == '__main__':

    # Start wxPython app
    app = wx.App()
    
    # Init window and add controls
    ex = MicFrame()
    ex.init_gui()
    ex.add_controls()

    backend = MicManager(ex)
    backend.setup()

    ex.Show()
    app.MainLoop()