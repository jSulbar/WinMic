# App class for winmic. Handles program's locale and its settings file
import wx
import os

class MicApp(wx.App):
    def __init__(self, appname):
        super().__init__()

        # Set appname for window label
        # and config name
        self.SetAppName(appname)

        # Make config file if it doesn't exist
        self.make_config_file()

        # Read locale from config file and set it
        lang = self.config.Read('language')
        self.locale = wx.Locale(int(lang))

        # Tell wxpython where to look for localization files
        wx.Locale.AddCatalogLookupPathPrefix('locale')
        self.locale.AddCatalog('i18n')

    def make_config_file(self):
        # Make directory in user's config dir
        # with the app's name
        std_paths = wx.StandardPaths.Get()
        cfg_path = std_paths.GetUserConfigDir()
        cfg_path = os.path.join(cfg_path, self.AppName)

        if not os.path.exists(cfg_path):
            os.mkdir(cfg_path)

        # Create config file through wx api
        self.config = wx.FileConfig(appName=self.AppName,
                                    localFilename=os.path.join(
                                    cfg_path, self.AppName))

        # Create language entry if it's not present.
        # config.Write value needs to be string, so convert enum
        if not self.config.HasEntry('language'):
            self.config.Write('language', str(wx.LANGUAGE_DEFAULT))
        
        # Save changes to file
        self.config.Flush()