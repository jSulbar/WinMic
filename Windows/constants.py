"""
Constant values for this program.
"""
import pyaudio
import wx

APP_NAME = 'WinMic'
DEFAULT_PORT = 12358

HOST_APIS = {
    'ASIO': pyaudio.paASIO,
    'DirectSound': pyaudio.paDirectSound,
    'MME': pyaudio.paMME,
    'PADevel': pyaudio.paInDevelopment
}

LOCALE_DIR_NAME = 'locale'
AVAILABLE_LANGS = {
    'Spanish': wx.LANGUAGE_SPANISH,
    'English': wx.LANGUAGE_ENGLISH
}
CATALOG_NAME = 'i18n'

CFGKEY_LANGUAGE = 'language'
CFGKEY_HOSTAPI = 'host_api'
CFGKEY_TRAY = 'minimize_to_tray'
DEFAULT_APP_CONFIG = {
    CFGKEY_LANGUAGE: str(wx.LANGUAGE_DEFAULT),
    CFGKEY_TRAY: 'True',
    CFGKEY_HOSTAPI: str(HOST_APIS['ASIO'])
}
CFG_FILENAME = 'cfg.ini'