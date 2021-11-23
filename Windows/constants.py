"""
Constant values for this program.
"""
import pyaudio
import wx

APP_NAME = 'WinMic'
DEFAULT_PORT = 12358

LOCALE_DIR_NAME = 'locale'
CATALOG_NAME = 'i18n'

DEFAULT_APP_CONFIG = {
    'language': str(wx.LANGUAGE_DEFAULT),
    'minimize_to_tray': 'True'
}
CFG_FILENAME = 'cfg.ini'