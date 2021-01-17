import wx
from wx.lib.intctrl import IntCtrl


class OrderQuantity(wx.BoxSizer):
    def __init__(self, parent, on_quantity_change):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

        self.on_quantity_change = on_quantity_change
        self.order_quantity_label = wx.StaticText(parent, label='Order Quantity: ')

        self.quantity_entry = IntCtrl(parent, wx.ID_ANY, 0, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        self.quantity_entry.SetMin(0)
        self.quantity_entry.SetNoneAllowed(True)
        self.Add(self.order_quantity_label, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 2)
        self.Add(self.quantity_entry, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 2)

        parent.Bind(wx.EVT_TEXT_ENTER, self.__on_enter, id=self.quantity_entry.GetId())

    def __on_enter(self, event):
        self.on_quantity_change(self.get_value())

    def get_value(self):
        return self.quantity_entry.GetValue()

    def make_invalid(self):
        self.quantity_entry.SetBackgroundColour(wx.RED)

    def make_valid(self):
        self.quantity_entry.SetBackgroundColour(wx.WHITE)


def test():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
    order = OrderQuantity(frame, None)

    frame.SetSizer(order)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    test()
