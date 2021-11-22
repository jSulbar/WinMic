
"""Module containing constants that define what controls each layout of this app have, and
the data necessary to create them. 'Layout' is defined as anything that could contain a group
of controls, such as a Frame."""

import wx

MAIN_WINDOW_LAYOUT = [
        {
            'control': {
                'class': wx.StaticText,
                'name': 'ip_label',
                'label': 'Your IPv4 address is: '
            },
            'psizer_args': (0, wx.ALIGN_CENTER | wx.ALL, 5),
            'csizer_args': (0, wx.ALL | wx.ALIGN_CENTER, 5)
        },
        {
            'controls': [
                {
                    'class': wx.Button,
                    'name': 'start_button',
                    'label': 'Start recording'
                },
                {
                    'class': wx.Button,
                    'name': 'stop_button',
                    'label': 'Stop recording',
                    'setup': lambda btn: btn.Disable()
                }
            ],
            'psizer_args': (1, wx.EXPAND, 5),
            'csizer_args': (1, wx.ALIGN_BOTTOM | wx.ALL, 5)
        }
    ]