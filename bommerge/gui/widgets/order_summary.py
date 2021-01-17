import wx

try:
    from gui.widgets.priceWidget import PriceWidget
except ImportError:
    from .priceWidget import PriceWidget


class OrderSummary(wx.StaticBoxSizer):
    def __init__(self, parent, shops_list):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, label="Order summary")
        self.parent = parent
        self.total_price_label = PriceWidget(parent, 'Total price')
        self.shop_price_label = {}
        self.flex_grid_sizer = wx.FlexGridSizer(3, 2, 5, 15)
        self.create_shop_label(shops_list)
        self.Add(self.flex_grid_sizer, 0, wx.ALL, 5)
        self.Add(self.total_price_label, 0, wx.ALL, 5)

    def create_shop_label(self, shops):
        for i, shop in enumerate(shops):
            label = PriceWidget(self.parent, shop)
            self.flex_grid_sizer.Add(label)
            self.shop_price_label[shop] = label

    def update(self, shop, price, total_price):
        self.shop_price_label[shop].update(price)
        self.total_price_label.update(total_price)
        self.Layout()


def test():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
    order = OrderSummary(frame, ['TME', 'Farnel', 'Mouser', 'RS Components'])
    order.update('Farnel', 10, 20)
    frame.SetSizer(order)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    test()
