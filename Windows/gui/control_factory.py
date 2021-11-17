"""Contains code that handles the logic for creating controls as defined on layout_definitions.py."""
from typing import Type
import wx


class ControlFactory:
    """Creates wxPython controls given a layout definition, following a given format. 
    The definitions for this program's layouts can be found inside layout_definitions.py.
    Needs a parent to construct objects because wxPython won't allow parentless objects and
    control.Reparent(window) won't work because ????"""
    def __init__(self, parent):
        self._parent = parent

    def get_controls(self, defs):
        """Takes a layout definition. Updates its 'control' entries with actual wxPython controls, using
        the data they provide for construction. Checking if they're valid using ControlDefValidator before 
        using this method is recommended."""
        new_defs = []
        for element in defs:
            updated_element = self._make_ctrl_dict(element)
            new_defs.append(updated_element)
        return new_defs

    def _make_ctrl_dict(self, element):
        """Replaces a 'control' dict with a wxPython control created using its data."""

        # Update the dict differently based on whether it has multiple controls
        # or a single one.
        if 'controls' in element:
            ctrl_dict = element.copy()
            ctrl_dict['controls'] = {}

            for ctrl in element['controls']:
                ctrl_dict['controls'][ctrl['name']] = self._make_control(ctrl)
            return ctrl_dict

        elif 'control' in element:
            ctrl_dict = element.copy()
            ctrl_dict['name'] = element['control']['name']
            ctrl_dict['control'] = self._make_control(ctrl_dict['control'])
            return ctrl_dict

    def _make_control(self, ctrl):
        """Creates the actual wxPython object, using the label and setup callback provided
        by its dict."""
        # Makes an object using the label provided.
        ctrl_obj = ctrl['class'](self._parent, label=ctrl['label'])
        if 'setup' in ctrl:
            ctrl['setup'](ctrl_obj)
        return ctrl_obj