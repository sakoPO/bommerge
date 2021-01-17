import wx


class Parameters(wx.StaticBoxSizer):
    def __init__(self, parent, parameters):
        wx.StaticBoxSizer.__init__(self, wx.VERTICAL, parent, label="Parameters")
        self.parent = parent
        self.variable = {}
        self.label = {}
        self.update(parameters)

    def update(self, parameters):
        for parameter in parameters:
            if parameters[parameter] is not None:
                self.variable[parameter] = parameter + ': ' + parameters[parameter]
                if parameter in self.label:
                    self.label[parameter].SetLabel(self.variable[parameter])
                else:
                    self.label[parameter] = wx.StaticText(self.parent, label=self.variable[parameter])
                    self.Add(self.label[parameter], 0, wx.ALL, 3)

        for label in self.label:
            self.label[label].Show(label in parameters)


def test():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
    parameters = {
        "Capacitance": "10uF",
        "Capacitors series": "GRM",
        "Case - inch": "0805",
        "Case - mm": "2012",
        "Dielectric": "X7R",
        "Kind of capacitor": "MLCC",
        "Manufacturer": "MURATA",
        "Manufacturer Part Number": "GRM21BR71A106KE51L",
        "Mounting": "SMD",
        "Operating temperature": "-55...125\u00b0C",
        "Operating voltage": "10V",
        "Tolerance": "10",
        "Type of capacitor": "ceramic"
    }
    order = Parameters(frame, parameters)
    frame.SetSizer(order)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    test()
