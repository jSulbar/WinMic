import wx

# Custom sizer to help manage and search for elements
class ChildSizer(wx.BoxSizer):
    def __init__(self, sizer = wx.HORIZONTAL) -> None:
        super().__init__(sizer)
        # Dict with every control that has been added
        # To this sizer
        self.control_list = {}

    # Adds control to list, then to wx.boxsizer instance
    def add_control(self, control, name, *args):
        if name in self.control_list.keys():
            raise Exception('A control with the given name already exists')
        self.control_list[name] = control
        self.Add(control, *args)

    # Returns the control with the given name
    def get_control(self, name):
        return self.control_list[name]


# A parent sizer class to hold other sizers,
# and to make it less repetitive to add controls
class ParentSizer(wx.BoxSizer):
    def __init__(self, sizer = wx.VERTICAL) -> None:
        super().__init__(sizer)
        # List of child sizers to keep track of
        self._csizer_list = []

    # Add child to this sizer
    def add_sizer(self, sizer, *args):
        # Only accept ChildSizers
        if type(sizer) is not ChildSizer:
            raise TypeError('Argument is not an instance of ChildSizer')

        # Add to list
        self._csizer_list.append(sizer)
        self.Add(sizer, *args)

    # Search inside child sizers for a control
    # with the given name
    def control_by_name(self, name):
        for childsizer in self._csizer_list:
            for key in childsizer.control_list:
                if key == name:
                    return childsizer.control_list[name]

    # Create empty sizers in bulk
    def bulk_add_sizers(self, proportion, flag, border, *sizers):
        for sizer in sizers:
            self.add_sizer(sizer, proportion, flag, border)

    # Add a new control
    def new_control(self, control, name, *, sizer_options, control_options):
        if isinstance(control, wx.Control):
            # Create a new sizer for it
            new_sizer = ChildSizer(wx.HORIZONTAL)
            new_sizer.add_control(control, name, *control_options)

            self.add_sizer(new_sizer, *sizer_options)
        else:
            raise TypeError('Argument must be a wxWidgets control')

    # Add multiple controls and put them inside a single sizer
    # Takes a dict formatted as { "controlname":control }
    def new_controls_row(self, controls, *, sizer_options, control_options):
        if type(controls) is dict:
            new_sizer = ChildSizer(wx.HORIZONTAL)

            for key in controls:
                new_sizer.add_control(controls[key], key, *control_options)

            self.add_sizer(new_sizer, *sizer_options)
        else:
            raise TypeError('Argument must be dict in the format { "controlname":control }')