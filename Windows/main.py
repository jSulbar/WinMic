import wx
from gui.app_frame import MicFrame
from client.gui_backend import BackendConnector


if __name__ == '__main__':

    # Start wxPython app
    app = wx.App()
    
    # Init window and add controls
    window = MicFrame()
    window.init_gui()
    window.add_controls()

    backend = BackendConnector(window)
    backend.setup()

    window.Show()
    app.MainLoop()