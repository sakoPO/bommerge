import wx


class PriceWidget(wx.BoxSizer):
    def __init__(self, parent, shop_name):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

        self.shop_name_label = wx.StaticText(parent, label=shop_name + ': ')
        self.price_label = wx.StaticText(parent, label="")
        self.currency_label = wx.StaticText(parent, label=' PLN')
        self.Add(self.shop_name_label)
        self.Add(self.price_label)
        self.Add(self.currency_label)

    def update(self, value):
        self.price_label.SetLabel('%.4f' % value)


def test():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
    order = PriceWidget(frame, "Test Distributor")
    frame.SetSizer(order)
    frame.Show()
    order.update(10)
    app.MainLoop()


if __name__ == "__main__":
    test()
