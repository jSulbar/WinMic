from gui.app_frame import MicFrame
from client.gui_backend import BackendConnector
from client.mic_app import MicApp


if __name__ == '__main__':

    # Start wxPython app
    app = MicApp(appname='WinMic')
    
    # Init window and add controls
    window = MicFrame()
    window.init_gui()
    window.add_controls()

    backend = BackendConnector(window, app)
    backend.setup()

    window.Show()
    app.MainLoop()