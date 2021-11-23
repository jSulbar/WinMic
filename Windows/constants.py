"""
Constant values for this program.
"""
import pyaudio
import wx

APP_NAME = 'WinMic'
DEFAULT_PORT = 12358

LOCALE_DIR_NAME = 'locale'
AVAILABLE_LANGS = {
    'es': wx.LANGUAGE_SPANISH,
    'en': wx.LANGUAGE_ENGLISH
}
CATALOG_NAME = 'i18n'

CFGKEY_LANGUAGE = 'language'
CFGKEY_TRAY = 'minimize_to_tray'
DEFAULT_APP_CONFIG = {
    CFGKEY_LANGUAGE: str(wx.LANGUAGE_DEFAULT),
    CFGKEY_TRAY: 'True'
}
CFG_FILENAME = 'cfg.ini'