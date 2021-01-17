import wx


class OrderInfo(wx.StaticBoxSizer):
    def __init__(self, parent, order_info_data):
        wx.StaticBoxSizer.__init__(self, wx.VERTICAL, parent, label="Order information")
        self.min_order_label = wx.StaticText(parent, label='Minimal Order:')
        self.mul_order_label = wx.StaticText(parent, label='Multiplicity:')
        self.stock_level = wx.StaticText(parent, label='Stock level:')
        self.min_order_value = wx.StaticText(parent, label="")
        self.mul_order_value = wx.StaticText(parent, label="")
        self.stock_level_value = wx.StaticText(parent, label="")

        sizer = wx.FlexGridSizer(3, 2, 5, 5)

        border = 0
        sizer.Add(self.min_order_label, 0, wx.ALL, border)
        sizer.Add(self.min_order_value, 0, wx.ALL, border)
        sizer.Add(self.mul_order_label, 0, wx.ALL, border)
        sizer.Add(self.mul_order_value, 0, wx.ALL, border)
        sizer.Add(self.stock_level, 0, wx.ALL, border)
        sizer.Add(self.stock_level_value, 0, wx.ALL, border)
        self.Add(sizer, 0, wx.ALL | wx.FIXED_MINSIZE, border=6)
        self.update(order_info_data)

    def update(self, order_info_data):
        self.min_order_value.SetLabel(str(order_info_data['MinAmount']))
        self.mul_order_value.SetLabel(str(order_info_data['Multiples']))
        self.stock_level_value.SetLabel(str(order_info_data['StockCount']))


def test():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
    order_info = {"MinAmount": 1, "Multiples": 1, "StockCount": 1}
    order = OrderInfo(frame, order_info)
    frame.SetSizer(order)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    test()
