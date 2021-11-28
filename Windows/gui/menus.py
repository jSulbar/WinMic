"""
Menus for the main window's menu bar control.
"""
import wx
from constants import AVAILABLE_LANGS, HOST_APIS

# Alias for gettext parsing
_ = wx.GetTranslation

class OptionsMenu(wx.Menu):
    """
    Allows the user to change the program's configuration.
    """
    def __init__(self, tray_enabled, lang, host_api):
        super().__init__()
        self.seen_prompt = False
        self._tray_setting(tray_enabled)
        self._hostapi_menu(host_api)
        self._make_lang_menu(lang)

    def _hostapi_menu(self, host_api):
        self.apimenu = wx.Menu()
        self.apimenu_items = {}
        for key in HOST_APIS:
            item = self.apimenu.AppendRadioItem(wx.ID_ANY, _(key))
            if host_api == HOST_APIS[key]:
                item.Check(True)
            self.apimenu_items[key] = item
            self.menu.Bind(wx.EVT_MENU, self._show_restart_prompt, item)
        self.Append(wx.ID_ANY, _('Host API'), self.apimenu)

    def _tray_setting(self, tray_enabled):
        self.minimize_to_tray = self.AppendCheckItem(wx.ID_ANY, _('Minimize to tray on window close'))
        if tray_enabled:
            self.minimize_to_tray.Check(True)

    def _show_restart_prompt(self, event):
        # Only show prompt once
        if not self.seen_prompt:
            wx.MessageBox(_('You will need to restart the program for this change to take effect.'))
            self.seen_prompt = True
        event.Skip()            
    
    def _make_lang_menu(self, lang):
        """
        Makes a menu for switching the app's language. Checks the current language.
        """
        self.langmenu = wx.Menu()
        self.langmenu_items = {}
        for key in AVAILABLE_LANGS:
            item = self.langmenu.AppendRadioItem(wx.ID_ANY, _(key))

            if AVAILABLE_LANGS[key] == lang:
                item.Check(True)

            self.langmenu_items[key] = item
            self.langmenu.Bind(wx.EVT_MENU, self._show_restart_prompt, self.langmenu_items[key])
        self.Append(wx.ID_ANY, _('Language'), self.langmenu)