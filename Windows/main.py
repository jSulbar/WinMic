import wx
from gui.app_frame import MicFrame
from client.mic_backend import MicBackend


if __name__ == '__main__':

    # Start wxPython app
    app = wx.App()
    
    # Init window and add controls
    ex = MicFrame()
    ex.init_gui()
    ex.add_controls()

    backend = MicBackend(ex)
    backend.setup()

    ex.Show()
    app.MainLoop()