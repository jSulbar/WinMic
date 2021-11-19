import wx

class UIEventBinder:
    def __init__(self, ctrl_list):
        self.ctrls = self._parse_ctrls(ctrl_list)

    def bind_controls(self):
        for key in self._callbacks:
            self.ctrls[key].Bind(
                self._callbacks[key]['event_type'], 
                lambda e, key=key: self._callbacks[key]['invoke'](**self._callbacks[key]['args'])
                )

    def _parse_ctrls(self, ctrl_defs):
        ctrls_dict = {}
        for ctrl in ctrl_defs:
            if 'control' in ctrl:
                ctrls_dict[ctrl['name']] = ctrl['control']
            elif 'controls' in ctrl:
                for key in ctrl['controls']:
                    ctrls_dict[key] = ctrl['controls'][key]
        return ctrls_dict