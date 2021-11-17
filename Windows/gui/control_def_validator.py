import wx


class ControlDefValidator:
    """Class to handle verification of control definitions."""

    def validate_defs(self, defs, sizer_check = True):
        """Checks a list of wxpython control definitions, returns a bool representing
        if validation was succesful. It takes 2 arguments:\n
        defs: Control data to be checked for validity.\n
        sizer_check: Tells the method whether it should return false if no data necessary for
        wx sizers is included with each control."""
        # Loop through each control
        for element in defs:
            # Check the control's properties
            if 'control' in element:
                if not self._validate_ctrl_def(element['control']):
                    return False
            elif 'controls' in element:
                for control in element['controls']:
                    if not self._validate_ctrl_def(control):
                        return False
            else:
                return False
            
            if sizer_check:
                # If there's no arguments to add the control(s) to a nested sizer,
                # return false.
                if not 'psizer_args' in element and not 'csizer_args' in element:
                    return False
        return True

    def _validate_ctrl_def(self, ctrl_dict):
        """Takes as argument a dictionary defining a wxPython control. Checks if it has
        the necessary values for creating a control, returns false if not."""

        # Check if class value is a valid wx.Control that can be constructed
        if type(ctrl_dict['class']) is not wx.Control:
            return False
        elif not 'name' in ctrl_dict:
            return False