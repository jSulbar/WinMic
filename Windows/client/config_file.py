"""
Config file creation and handling for this application.
"""
import wx
import os

class WinMicConfig(wx.FileConfig):
    """
    Subclass of wx.FileConfig with a few extra functions specific to this app.
    Creates a default config file on initialization, if not already present.
    """
    def __init__(self, appname, filename, defaults):
        self.setup_cfg_path(appname)
        super().__init__(appName = appname,
                        localFilename=os.path.join(self.path, filename))
        self.create_default_cfg(defaults)

    def setup_cfg_path(self, appname):
        """
        Sets up the fileconfig path. Uses the standard user configuration folder.
        """
        sp = wx.StandardPaths.Get()
        self.path = sp.GetUserConfigDir()
        self.path = os.path.join(self.path, appname)

        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def create_default_cfg(self, cfg_template):
        """
        Creates a configuration file using a dictionary containing the
        default values for each key. Only writes keys missing from current
        config, if any.
        """

        for key in cfg_template:
            if not self.HasEntry(key):
                self.Write(key, cfg_template[key])
            
        self.Flush()