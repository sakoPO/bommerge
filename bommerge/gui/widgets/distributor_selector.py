import wx


class DistributorSelector(wx.RadioBox):
    def __init__(self, parent, on_distributor_change=None):
        self.distributor = ['None', 'PartKeepr', 'TME', 'RS Components', 'Farnel', 'Mouser']
        wx.RadioBox.__init__(self, parent, label="Distributor selection", choices=self.distributor, majorDimension=2,
                             style=wx.RA_SPECIFY_ROWS)

        self.on_distributor_change = on_distributor_change

        self.Bind(wx.EVT_RADIOBOX, self.__on_selection, id=self.GetId())

    def activate(self, distributors):
        for i, distributor in enumerate(self.distributor):
            self.EnableItem(i, distributor in distributors)

    def get(self):
        return self.distributor[self.GetSelection()]

    def __on_selection(self, event):
        # print("selected: " + str(self.GetSelection()))
        if self.on_distributor_change:
            self.on_distributor_change(self.get())


def test():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
    order = DistributorSelector(frame)
    order.activate(['TME', 'Farnel', 'Mouser', 'RS Components'])
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    test()
