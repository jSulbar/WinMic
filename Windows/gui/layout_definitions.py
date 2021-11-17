
"""Module containing constants that define what controls each layout of this app have, and
the data necessary to create them. 'Layout' is defined as anything that could contain a group
of controls, such as a Frame."""

import wx

# Create alias for gettext parsing
_ = wx.GetTranslation

MIC_FRAME_LAYOUT = [
        {
            'control': {
                'class': wx.StaticText,
                'name': 'ip_label',
                'label': _('Your IPv4 address is: ')
            },
            'psizer_args': (0, wx.ALIGN_LEFT | wx.ALL, 5),
            'csizer_args': (0, wx.ALL | wx.ALIGN_CENTER, 5)
        },
        {
            'control': {
                'class': wx.CheckBox,
                'name': 'tray_checkbox',
                'label': _('Hide to tray on window close')
            },
            'psizer_args': (1, wx.ALL | wx.ALIGN_LEFT, 5),
            'csizer_args': (0, wx.ALIGN_LEFT | wx.ALL, 5)
        },
                {
            'controls': [
                {
                    'class': wx.Button,
                    'name': 'start_button',
                    'label': _('Start recording')
                },
                {
                    'class': wx.Button,
                    'name': 'stop_button',
                    'label': _('Stop recording'),
                    'setup': lambda btn: btn.Disable()
                }
            ],
            'psizer_args': (1, wx.EXPAND, 5),
            'csizer_args': (1, wx.ALIGN_BOTTOM | wx.ALL, 5)
        }
    ]