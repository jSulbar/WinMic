import wx
from constants import LOCALE_DIR_NAME, CATALOG_NAME

class WinMicApp(wx.App):
    def __init__(self):
        super().__init__()

    def set_lang(self, lang):
        """
        Sets the language for this application. This is needed
        for wx's Gettext to actually translate the strings given to it.
        """
        self.locale = wx.Locale(lang)

        wx.Locale.AddCatalogLookupPathPrefix(LOCALE_DIR_NAME)
        self.locale.AddCatalog(CATALOG_NAME)