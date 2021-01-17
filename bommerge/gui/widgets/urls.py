import wx
import wx.adv


class Urls(wx.BoxSizer):
    def __init__(self, parent, partinfo_url, datasheat_url):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.shop_label = wx.adv.HyperlinkCtrl(parent, label=u"Component page")
        self.datasheat_label = wx.adv.HyperlinkCtrl(parent, label=u"Datasheat")
        self.Add(self.shop_label)
        self.Add(self.datasheat_label)
        self.update(partinfo_url, datasheat_url)

    def update(self, partinfo_url, datasheat_url):
        if partinfo_url:
            self.shop_label.SetURL(partinfo_url)
        if datasheat_url:
            self.datasheat_label.SetURL(datasheat_url)

        self.shop_label.Enable(partinfo_url != "")
        self.datasheat_label.Enable(datasheat_url != "")


def main():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
    order = Urls(frame, "a", "")
    frame.SetSizer(order)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
