import wx

try:
    from gui.widgets import componentListWidget as componentList
    from gui.widgets.parameters import Parameters
    from gui.widgets.price_range import PriceRange
    from gui.widgets.order_info import OrderInfo as OrderInfoWidget
    from gui.widgets.urls import Urls as UrlsWidget
except ImportError:
    try:
        from widgets import componentListWidget as componentList
        from widgets.parameters import Parameters
        from widgets.price_range import PriceRange
        from widgets.order_info import OrderInfo as OrderInfoWidget
        from widgets.urls import Urls as UrlsWidget
    except ImportError:
        from parameters import Parameters
        import componentListWidget as componentList
        from price_range import PriceRange
        from order_info import OrderInfo as OrderInfoWidget
        from urls import Urls as UrlsWidget


class SupplierInfo(wx.Panel):
    def __init__(self, parent, supplier_name, components, on_active_component_change):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.validate = None
        self.components = None
        self.parts = components
        self.on_change = on_active_component_change
        self.active_part = self.parts[0]
        self.active_part_index = 0
        if len(self.parts) > 1:
            self.create_component_list()
        sizer = self.create_component_details()

        # layout
        if self.components:
            self.main_sizer.Add(self.components, 1, wx.ALL | wx.EXPAND, 10)
        self.main_sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(self.main_sizer)

    def get_active_part_index(self):
        return self.active_part_index

    @staticmethod
    def add_description(self, component):
        desc = ''
        for parameter in component['Parameters']:
            desc = component['Parameters'][parameter] + '; ' + desc
        component['Description'] = desc

    def create_component_list(self):
        columns = ['Manufacturer Part Number', 'Description', 'Price']
        self.components = componentList.ScrolledComponentsList_v3(parent=self, columns=columns,
                                                                  on_selection_change=self.on_selection_change,
                                                                  on_item_double_click=self.on_item_double_click,
                                                                  flags=wx.LC_SINGLE_SEL)

        self.components.add_data_geter(
            {'Manufacturer Part Number': lambda x: x['Parameters']['Manufacturer Part Number']})
        self.refresh_component_list()

    def refresh_component_list(self):
        self.components.remove_all_items()
        self.components.add_items(self.parts, None)
        self.components.SetItemBackgroundColour(self.active_part_index, wx.GREEN)
        self.components.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.components.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.components.SetColumnWidth(2, wx.LIST_AUTOSIZE)

    def create_component_details(self):
        self.parameters = Parameters(self, self.active_part['Parameters'])
        self.price_order = self.create_price_order_urls()
        parameters_price_order_url_sizer = wx.BoxSizer(wx.HORIZONTAL)
        parameters_price_order_url_sizer.Add(self.parameters, 1, wx.EXPAND | wx.ALL, 5)
        parameters_price_order_url_sizer.Add(self.price_order, 1, wx.EXPAND | wx.ALL, 5)
        return parameters_price_order_url_sizer

    def create_price_order_urls(self):
        self.price_range = PriceRange(self, self.active_part['PriceRanges'])
        self.order_info = OrderInfoWidget(self, self.active_part['OrderInfo'])

        product_info_page = self.active_part['Links']['ProductInformationPage'] if 'ProductInformationPage' in \
                                                                                   self.active_part['Links'] else None
        self.urls = UrlsWidget(self, product_info_page, None)

        # layout
        price_range_and_order_info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        price_range_and_order_info_sizer.Add(self.price_range, 1, wx.EXPAND | wx.ALL, 5)
        price_range_and_order_info_sizer.Add(self.order_info, 1, wx.EXPAND | wx.ALL, 5)
        price_order_urls_sizer = wx.BoxSizer(wx.VERTICAL)
        price_order_urls_sizer.Add(price_range_and_order_info_sizer, 0, wx.ALL, 5)
        price_order_urls_sizer.Add(self.urls, 0, wx.ALL, 5)
        return price_order_urls_sizer

    def on_item_double_click(self, item_number):
        self.components.SetItemBackgroundColour(self.active_part_index, wx.WHITE)
        self.components.SetItemBackgroundColour(item_number, wx.GREEN)
        self.active_part_index = item_number
        self.active_part = self.parts[item_number]
        if self.on_change:
            self.on_change()

    def on_selection_change(self, item_number):
        part = self.parts[item_number]
        self.order_info.update(part['OrderInfo'])
        self.price_range.update(part['PriceRanges'])
        self.parameters.update(part['Parameters'])
        self.main_sizer.Layout()


def main():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

    Components = [
        {
            "Description": "Capacitor: ceramic; MLCC; 10uF; 10V; X7R; \u00b110%; SMD; 0805",
            "Links": {
                "Photo": "https://ce8dc832c.cloudimg.io/fit/640x480/fwk@16e51c215e1915554b0be79c406d0d5be2676b3e/_cdn_/DA/F2/B0/00/0/733101_1.jpg?mark_url=_tme-wrk_%2Ftme_new_render3d.png&mark_pos=center&mark_size=100pp",
                "ProductInformationPage": "https://www.tme.eu/en/details/cl21b106kpqnnng/0805-mlcc-smd-capacitors/samsung/",
                "Thumbnail": "https://ce8dc832c.cloudimg.io/fit/100x75/webp@7d4ea33fd0784ad2da926a90658ba45b300fcb7e/_cdn_/DA/F2/B0/00/0/733101_1.jpg"
            },
            "OrderInfo": {
                "MinAmount": 100,
                "Multiples": 100,
                "StockCount": 19400
            },
            "Parameters": {
                "Capacitance": "10uF",
                "Case - inch": "0805",
                "Case - mm": "2012",
                "Dielectric": "X7R",
                "Kind of capacitor": "MLCC",
                "Manufacturer": "SAMSUNG",
                "Manufacturer Part Number": "CL21B106KPQNNNG",
                "Mounting": "SMD",
                "Operating temperature": "-55...125\u00b0C",
                "Operating voltage": "10V",
                "Tolerance": "10",
                "Type of capacitor": "ceramic"
            },
            "PriceRanges": [
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
                }
            ],
            "Symbol": {
                "Symbol": "CL21B106KPQNNNG",
                "SymbolTME": "CL21B106KPQNNNG"
            }
        },
        {
            "Description": "Capacitor: ceramic; MLCC; 10uF; 10V; X7R; \u00b110%; SMD; 0805; Series: GRM",
            "Links": {
                "Photo": "https://ce8dc832c.cloudimg.io/fit/640x480/fwk@16e51c215e1915554b0be79c406d0d5be2676b3e/_cdn_/DA/F2/B0/00/0/733101_1.jpg?mark_url=_tme-wrk_%2Ftme_new_render3d.png&mark_pos=center&mark_size=100pp",
                "ProductInformationPage": "https://www.tme.eu/en/details/grm21br71a106ke51l/0805-mlcc-smd-capacitors/murata/",
                "Thumbnail": "https://ce8dc832c.cloudimg.io/fit/100x75/webp@7d4ea33fd0784ad2da926a90658ba45b300fcb7e/_cdn_/DA/F2/B0/00/0/733101_1.jpg"
            },
            "OrderInfo": {
                "MinAmount": 10,
                "Multiples": 10,
                "StockCount": 1048
            },
            "Parameters": {
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
            },
            "PriceRanges": [
                {
                    "Amount": 10,
                    "Price": 2.24107
                },
                {
                    "Amount": 100,
                    "Price": 1.418
                },
                {
                    "Amount": 1000,
                    "Price": 0.88122
                },
                {
                    "Amount": 3000,
                    "Price": 0.65309
                },
                {
                    "Amount": 12000,
                    "Price": 0.58599
                }
            ],
            "Symbol": {
                "Symbol": "GRM21BR71A106KE51L",
                "SymbolTME": "GRM21BR71A106KE51L"
            }
        }
    ]
    order = SupplierInfo(frame, "test supplier", Components, None)
    #    frame.SetSizer(order)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
