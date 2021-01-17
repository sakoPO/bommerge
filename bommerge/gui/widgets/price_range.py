import wx


class PriceRange(wx.StaticBoxSizer):
    def __init__(self, parent, ranges):
        wx.StaticBoxSizer.__init__(self, wx.VERTICAL, parent, label="Price Range")
        self.parent = parent
        self.amount_label = wx.StaticText(self.parent, label="Amount")
        self.price_label = wx.StaticText(self.parent, label="Price")
        self.flex_grid_sizer = wx.FlexGridSizer(2, 2, 20)
        self.flex_grid_sizer.Add(self.amount_label, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.flex_grid_sizer.Add(self.price_label, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.Add(self.flex_grid_sizer, 0, wx.ALL, 5)
        self.widgets = []
        self.update(ranges)

    def update(self, ranges):
        for i, price_range in enumerate(ranges):
            if i < len(self.widgets):
                self.widgets[i][0].SetLabel(str(price_range["Amount"]))
                self.widgets[i][1].SetLabel(str(price_range["Price"]))
            else:
                widgets = [wx.StaticText(self.parent, label=str(price_range["Amount"])),
                           wx.StaticText(self.parent, label=str(price_range["Price"]))]
                self.widgets.append(widgets)
                self.flex_grid_sizer.Add(widgets[0], 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
                self.flex_grid_sizer.Add(widgets[1], 0, wx.ALL, 0)

        for i, widgets in enumerate(self.widgets):
            widgets[0].Show(i < len(ranges))
            widgets[1].Show(i < len(ranges))


def test():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
    price_ranges = [
        {
            "Amount": 100,
            "Price": 0.24603
        },
        {
            "Amount": 1000,
            "Price": 0.1673
        },
        {
            "Amount": 3000,
            "Price": 0.13375
        },
        {
            "Amount": 15000,
            "Price": 0.12793
        }]
    order = PriceRange(frame, price_ranges)
    frame.SetSizer(order)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    test()
