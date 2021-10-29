import wx
from micserver_ui import MicWindow

def main():
    app = wx.App()
    ex = MicWindow()
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()