import wx


class PartDetailDialog(wx.Dialog):
    def __init__(self, parent, component, decoded):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Component details", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.result = None

        columns = self.sort_columns(list(component.keys()))
        if 'Designator' in columns:
            columns.remove('Designator')
        if 'validation_status' in columns:
            columns.remove('validation_status')

        if decoded == None:
            decoded = []

        self.components_table = self.__create_components_table(columns, component, decoded)
        self.partname_frame = self.create_frame_with_parameters_decoded_from_partname(decoded)
        self.origin_frame = self.create_origin_frame(component)
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(self.partname_frame, 1, wx.EXPAND | wx.ALL, 5)
        bottom_sizer.Add(self.origin_frame, 1, wx.EXPAND | wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.components_table, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.Layout()
        main_sizer.Fit(self)
        self.Centre(wx.BOTH)

    def sort_columns(self, columns):
        def sort(x):
            keys = {'Quantity': 1, 'Designator': 99}
            if x in keys:
                return keys[x]
            return 98

        columns.sort(key=sort)
        return columns

    def __create_components_table(self, columns, component, decoded):
        flex_grid_sizer = wx.FlexGridSizer(3, len(columns) + 1, 5, 5)
        # first line
        flex_grid_sizer.Add((0, 0), 0, wx.EXPAND | wx.ALL, 5)
        for column in columns:
            label = wx.StaticText(self, label=column)
            flex_grid_sizer.Add(label, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        # second line
        bom_parameters_label = wx.StaticText(self, label='BOM Parameters')
        flex_grid_sizer.Add(bom_parameters_label, 0, wx.EXPAND | wx.ALL, 3)
        for column in columns:
            entry = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,  wx.TE_READONLY)
            entry.SetMinSize(wx.Size(80, 25))
            if column in component and component[column]:
                entry.SetValue(str(component[column]))
            flex_grid_sizer.Add(entry, 0, wx.EXPAND | wx.ALL, 3)
        # third line
        decoded_parameters_label = wx.StaticText(self, label='Partname Parameters')
        flex_grid_sizer.Add(decoded_parameters_label, 0, wx.EXPAND | wx.ALL, 3)
        for column in columns:
            entry = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
            entry.SetMinSize(wx.Size(80, 25))
            if column in decoded and decoded[column]:
                entry.SetValue(decoded[column])
            flex_grid_sizer.Add(entry, 0, wx.EXPAND | wx.ALL, 3)
        return flex_grid_sizer

    def create_frame_with_parameters_decoded_from_partname(self, decoded_parameters):
        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label="Parameters decoded from partname")
        if not decoded_parameters:
            missing_part_number = wx.StaticText(self,
                                                label="Unable do decode parameters. Part number missing or unsupported part number.")
            sizer.Add(missing_part_number, 1, wx.EXPAND | wx.ALL, 3)
        else:
            for i, parameter in enumerate(decoded_parameters):
                name_label = wx.StaticText(self, label=str(parameter) + ': ' + str(decoded_parameters[parameter]))
                sizer.Add(name_label, 1, wx.EXPAND | wx.ALL, 3)
        return sizer

    def create_origin_frame(self, component):
        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label="Component orignin")
        for i, designators in enumerate(component['Designator'].splitlines()):
            name_label = wx.StaticText(self, wx.ID_ANY | wx.ALL, designators)
            sizer.Add(name_label, 1, wx.EXPAND | wx.ALL, 3)
        return sizer

    def cancel(self, event=None):
        pass


if __name__ == "__main__":
    app = wx.App()
    # Create open file dialog
    frame = PartDetailDialog(None, {"Capacitance": "10", 'Designator': "asdf"}, None)
    frame.ShowModal()
    app.MainLoop()
