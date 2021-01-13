import wx

mergedComponent = {}


class MergeDialog(wx.Dialog):
    def __init__(self, parent, columns, components):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Manual merging", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.parent = parent
        self.result = None

        components_table = self._createComponentsTable(columns, components)
        merged = self.mergeFields(components)
        [sizer, mergeFields] = self._createMergeFields(columns, merged)
        buttons = self._createButtons(mergeFields, merged)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(components_table, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(buttons, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.Layout()
        main_sizer.Fit(self)
        self.Centre(wx.BOTH)

    @staticmethod
    def sumQuantity(components):
        quantity = 0
        for component in components:
            quantity = quantity + int(component['Quantity'])
        return quantity

    @staticmethod
    def mergeDesignator(components):
        designator = ''
        for component in components:
            designator = designator + component['Designator']
        return designator

    def mergeFields(self, components):
        def replaceNone(fieldValue):
            if fieldValue:
                return fieldValue
            return ''

        merged = {}
        merged['Quantity'] = self.sumQuantity(components)
        merged['Designator'] = self.mergeDesignator(components)

        for component in components:
            for field in component.keys():
                if field in ['Quantity', 'Designator']:
                    continue
                if field not in merged:
                    merged[field] = set()

                merged[field].add(replaceNone(component[field]))
        return merged

    @staticmethod
    def merge(combos, merged):
        fields_to_skip = ['validation_status']
        for field in merged.keys():
            if field in fields_to_skip:
                continue
            if field in ['Quantity', 'Designator']:
                mergedComponent[field] = merged[field]
            elif isinstance(combos[field], wx.TextCtrl):
                mergedComponent[field] = combos[field].GetLineText(0)
            else:
                mergedComponent[field] = combos[field].GetStringSelection()
        return mergedComponent

    def _createComponentsTable(self, columns, components):
        parent = wx.FlexGridSizer(len(columns), 5, 5)  # ttk.Frame(self)
        # first line
        for column in columns:
            label = wx.StaticText(self, label=column)
            parent.Add(label, 1, wx.EXPAND | wx.ALL, 3)
        # components
        for component in components:
            for column in columns:
                entry = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
                entry.SetMinSize(wx.Size(80, 25))
                if component[column]:
                    entry.SetValue(str(component[column]))
                parent.Add(entry, 1, wx.EXPAND | wx.ALL, 3)
        return parent

    def _createMergeFields(self, columns, component):
        def createTextWidget(parent, text):
            textWidget = wx.TextCtrl(parent, wx.ID_ANY, text, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
            return textWidget

        def createEntryWidget(parent, value):
            entry = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
            if type(value) is set:
                entry.SetValue(list(component[column])[0])
            else:
                entry.SetValue(str(value))
            return entry

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label='Merged')
        sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
        flex_grid_sizer = wx.FlexGridSizer(len(columns), 5, 5)
        #first line
        for column in columns:
            label = wx.StaticText(self, label=column)
            flex_grid_sizer.Add(label, 1, wx.EXPAND | wx.ALL, 5)
        # second line
        mergeFields = {}
        for column in columns:
            if column == 'Designator':
                widget = wx.TextCtrl(self, wx.ID_ANY, component['Designator'], wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
            elif column == 'Quantity':
                widget = createEntryWidget(flex_grid_sizer, component[column])
            elif len(component[column]) == 1:
                widget = createEntryWidget(flex_grid_sizer, component[column])
            else:
                widget = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     list(component[column]))
            flex_grid_sizer.Add(widget, 1, wx.EXPAND | wx.ALL, 5)
            mergeFields[column] = widget

        sizer.Add(flex_grid_sizer, 1, wx.EXPAND | wx.ALL, 5)
        return [sizer, mergeFields]

    def _createButtons(self, combos, merged):
        def doMerge():
            self.result = self.merge(combos, merged)
            self.EndModal(1)

        parent = wx.BoxSizer(wx.HORIZONTAL)

        done_button = wx.Button(self, wx.ID_ANY, u"Done", wx.DefaultPosition, wx.DefaultSize, 0)
        done_button.Bind(wx.EVT_BUTTON, lambda x: doMerge())
        parent.Add(done_button)

        cancel_button = wx.Button(self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        parent.Add(cancel_button)
        return parent


if __name__ == "__main__":
    app = wx.App()
    # Create open file dialog
    frame = MergeDialog(None, ["Quantity", "Capacitance"],
                        [{"Quantity": "2", "Capacitance": "10", 'Designator': "asdf"},
                         {"Quantity": "10", "Capacitance": "20", 'Designator': "asdf"}])
    frame.ShowModal()
    app.MainLoop()
