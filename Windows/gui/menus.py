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
        self.apimenu, self.apimenu_items = self._menu_from_dict(HOST_APIS,
                                                                host_api,
                                                                self._show_restart_prompt)
        self.langmenu, self.langmenu_items = self._menu_from_dict(AVAILABLE_LANGS,
                                                                    lang,
                                                                    self._show_restart_prompt)
        self.Append(wx.ID_ANY, _('Host API'), self.apimenu)
        self.Append(wx.ID_ANY, _('Language'), self.langmenu)
    
    def _menu_from_dict(self, values_dict, default_value, callback = None):
        """
        Creates a menu with radio buttons given a dictionary.
        """
        menu = wx.Menu()
        menu_items = {}
        for key in values_dict:
            item = menu.AppendRadioItem(wx.ID_ANY, key)
            if values_dict == default_value:
                item.Check(True)
            menu_items[key] = item
            if callback:
                menu.Bind(wx.EVT_MENU, callback, item)
        return menu, menu_items

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