try:
    import gui.widgets.componentListWidget as componentList
    from gui.widgets import order_summary
    from gui.widgets.order_quantity import OrderQuantity
    from gui.widgets.distributor_selector import DistributorSelector
    from gui.widgets.supplier_info import SupplierInfo
except ImportError:
    try:
        import widgets.componentListWidget as componentList
        from widgets import order_summary
        from widgets.order_quantity import OrderQuantity
        from widgets.distributor_selector import DistributorSelector
        from widgets.supplier_info import SupplierInfo
    except ImportError:
        import componentListWidget as componentList
        import order_summary
        from order_quantity import OrderQuantity
        from distributor_selector import DistributorSelector
        from supplier_info import SupplierInfo

import wx
import wx.aui


class SuppliersDetailsWidget(wx.Panel):
    def __init__(self, parent, distributors, on_order_change):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.components = distributors  # dictionary: { "distributor name": [component1, component2, ...] }
        self.on_order_change_callback = on_order_change
        self.supplier = {}
        self.order_quantity_widget = OrderQuantity(self, self.__on_quantity_change)
        self.create_distributor_selector()
        self.distributors_notebook = wx.aui.AuiNotebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                        wx.aui.AUI_NB_DEFAULT_STYLE)
        self.distributors_notebook.SetMinSize((200, 500))
        for distributor in distributors:
            supplier = SupplierInfo(self.distributors_notebook, distributor, distributors[distributor], self._on_change)
            self.supplier[distributor] = supplier
            self.distributors_notebook.AddPage(supplier, distributor, False, wx.NullBitmap)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.order_quantity_widget, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(self.distributor_selector, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(self.distributors_notebook, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.main_sizer)

    def create_distributor_selector(self):
        self.distributor_selector = DistributorSelector(self, self._on_distributor_change)
        distributors = ['None']
        for distributor in self.components:
            distributors.append(distributor)
        self.distributor_selector.activate(distributors)

    def validate_quantity(self, component):
        quantity = self.order_quantity_widget.get_value()
        order_info = component['OrderInfo']
        if not quantity or quantity < order_info['MinAmount']:
            return False
        if (quantity - order_info['MinAmount']) % order_info['Multiples'] != 0:
            return False
        return True

    def get_component_by_distributor(self, distributor_name):
        print("Loking for component from: " + distributor_name)
        if distributor_name != "None":
            return self.components[distributor_name][self.supplier[distributor_name].get_active_part_index()]

    def __update_order_info(self, distributor_name):
        component = self.get_component_by_distributor(distributor_name)
        if distributor_name not in ['None', 'PartKeeper']:
            if not self.validate_quantity(component):
                self.order_quantity_widget.make_invalid()
                return

        self.order_quantity_widget.make_valid()
        quantity = 0 if distributor_name == 'None' else self.order_quantity_widget.get_value()
        part_index = None if distributor_name == 'None' else self.supplier[distributor_name].get_active_part_index()
        if self.on_order_change_callback:
            self.on_order_change_callback(distributor_name, quantity, part_index)

    def _on_distributor_change(self, distributor):
        self.__update_order_info(distributor)

    def __on_quantity_change(self, quantity):
        self.__update_order_info(self.distributor_selector.get())

    def _on_change(self):
        self.__update_order_info(self.distributor_selector.get())


def main():
    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 600),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

    distributors = [{
        "Components": [
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
        ],
        "Name": "TME"
    },
        {
            "Components": [
                {
                    "Description": "Capacitor MLCC 10uF \u00b110% 25V X7R 1206",
                    "Links": {
                        "Photo": "https:",
                        "ProductInformationPage": "https:",
                        "Thumbnail": "https:"
                    },
                    "OrderInfo": {
                        "MinAmount": 1,
                        "Multiples": 1,
                        "StockCount": 0
                    },
                    "Parameters": {
                        "Capacitance": "10uF",
                        "Capacitor Type": "MLCC",
                        "Dielectric Type": "X7R",
                        "Manufacturer": "Unknown",
                        "Manufacturer Part Number": "Unknown",
                        "Storage Location": "BOX2",
                        "Tolerance": "10",
                        "Voltage": "25V"
                    },
                    "PriceRanges": [
                        {
                            "Amount": 1,
                            "Price": None
                        }
                    ],
                    "Symbol": {
                        "Name": "10uF"
                    }
                },
                {
                    "Description": "Capacitor MLCC 10uF \u00b15% 10V X7R -55..125\u2103 0805",
                    "Links": {
                        "Photo": "https:",
                        "ProductInformationPage": "https:",
                        "Thumbnail": "https:"
                    },
                    "OrderInfo": {
                        "MinAmount": 1,
                        "Multiples": 1,
                        "StockCount": 0
                    },
                    "Parameters": {
                        "Capacitance": "10uF",
                        "Capacitor Type": "MLCC",
                        "Dielectric Type": "X7R",
                        "Manufacturer": "Kemet",
                        "Manufacturer Part Number": "C0805C106J8RACAUTO",
                        "Storage Location": "BOX2",
                        "Tolerance": "5",
                        "Voltage": "10V"
                    },
                    "PriceRanges": [
                        {
                            "Amount": 1,
                            "Price": "0.0000"
                        }
                    ],
                    "Symbol": {
                        "Name": "C0805C106J8RACAUTO"
                    }
                },
                {
                    "Description": "Capacitor MLCC 10uF \u00b110% 35V X7R -55..125\u2103 1210",
                    "Links": {
                        "Photo": "https:",
                        "ProductInformationPage": "https:",
                        "Thumbnail": "https:"
                    },
                    "OrderInfo": {
                        "MinAmount": 1,
                        "Multiples": 1,
                        "StockCount": 2
                    },
                    "Parameters": {
                        "Capacitance": "10uF",
                        "Capacitor Type": "MLCC",
                        "Dielectric Type": "X7R",
                        "Manufacturer": "Samsung",
                        "Manufacturer Part Number": "CL32B106KLULNNE",
                        "Storage Location": "BOX2",
                        "Tolerance": "10",
                        "Voltage": "35V"
                    },
                    "PriceRanges": [
                        {
                            "Amount": 1,
                            "Price": "0.0000"
                        }
                    ],
                    "Symbol": {
                        "Name": "CL32B106KLULNNE"
                    }
                },
                {
                    "Description": "Capacitor MLCC 10uF \u00b120% 50V X7R -55..125\u2103 1210",
                    "Links": {
                        "Photo": "https:",
                        "ProductInformationPage": "https:",
                        "Thumbnail": "https:"
                    },
                    "OrderInfo": {
                        "MinAmount": 1,
                        "Multiples": 1,
                        "StockCount": 0
                    },
                    "Parameters": {
                        "Capacitance": "10uF",
                        "Capacitor Type": "MLCC",
                        "Datasheet URL": "https://spicat.avx.com/product/mlcc/chartview/12105C106MAT2A/DataSheet/X7R",
                        "Dielectric Type": "X7R",
                        "Manufacturer": "AVX",
                        "Manufacturer Part Number": "12105C106MAT2A",
                        "Product URL": "https://spicat.avx.com/product/mlcc/chartview/12105C106MAT2A",
                        "Storage Location": "limbo",
                        "Tolerance": "20",
                        "Voltage": "50V",
                        "Working Temperature": "None"
                    },
                    "PriceRanges": [
                        {
                            "Amount": 1,
                            "Price": None
                        }
                    ],
                    "Symbol": {
                        "Name": "12105C106MAT2A"
                    }
                }
            ],
            "Name": "PartKeepr"
        }]

    order = SuppliersDetailsWidget(frame, distributors, None)
    frame.Layout()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
