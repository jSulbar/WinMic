import wx

# Custom sizer to help manage and search for elements
class ChildSizer(wx.BoxSizer):
    """Custom BoxSizer to be contained inside a ParentSizer instance. Controls should be added with
    csizer.add_control() instead of wxPython's default sizer.Add(). Each control must be added with
    an unique name to identify it. These can then be retrieved anytime using csizer.get_control."""
    def __init__(self) -> None:
        super().__init__(wx.HORIZONTAL)
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
    """Custom BoxSizer that contains ChildSizer instances inside of itself. Controls should be
    added with psizer.new_control() or psizer.new_controls_row(). It implicitly creates a new ChildSizer
    with each control or controls added to avoid verbose object creation and handling, and maintains
    references to each control added which can then be retrieved with control_by_name()."""
    def __init__(self) -> None:
        super().__init__(wx.VERTICAL)
        # List of child sizers to keep track of
        self._csizer_list = []

    # Add child to this sizer
    def _add_sizer(self, sizer, *args):
        # Only accept ChildSizers
        if type(sizer) is not ChildSizer:
            raise TypeError('Argument is not an instance of ChildSizer')

        # Add to list
        self._csizer_list.append(sizer)
        self.Add(sizer, *args)

    # Search inside child sizers for a control
    # with the given name
    def control_by_name(self, name):
        """Returns a control added to this sizer, by searching for a control with
        the name provided."""
        for childsizer in self._csizer_list:
            for key in childsizer.control_list:
                if key == name:
                    return childsizer.control_list[name]

    # Add a new control
    def new_control(self, control, name, *, sizer_options, control_options):
        """Adds a new control to this sizer, creating a new ChildSizer containing it. 
        Takes arguments as follows:\n

        control: The new wx.Control added.\n

        name: An identifying string used to search the control with control_by_name().\n

        sizer_options: A tuple containing arguments that determine how the new ChildSizer created
        will fit into this ParentSizer. See wxPython.BoxSizer docs for possible values.\n   

        control_options: A tuple with arguments defining how the new controls will fit
        into the new ChildSizer."""
        if isinstance(control, wx.Control):
            # Create a new sizer for it
            new_sizer = ChildSizer()
            new_sizer.add_control(control, name, *control_options)

            self._add_sizer(new_sizer, *sizer_options)
        else:
            raise TypeError('Argument must be a wxWidgets control')

    # Add multiple controls and put them inside a single sizer
    # Takes a dict formatted as { "controlname":control }
    def new_controls_row(self, controls, *, sizer_options, control_options):
        """Adds many controls to this sizer, creating a single ChildSizer containg each control.
        Takes arguments as follows:\n

        controls: Takes a dictionary, with each key being the control's identifying name and
        their values containing the control object.\n

        sizer_options: A tuple containing arguments that determine how the new ChildSizer will fit
        into this ParentSizer. See wxPython.BoxSizer docs for possible values.\n

        control_options: A tuple with arguments defining how the new controls will fit
        into the new ChildSizer."""
        if type(controls) is dict:
            new_sizer = ChildSizer()

            for key in controls:
                new_sizer.add_control(controls[key], key, *control_options)

            self._add_sizer(new_sizer, *sizer_options)
        else:
            raise TypeError('Argument must be dict in the format { "controlname":control }')