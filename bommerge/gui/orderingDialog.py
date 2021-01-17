try:
    import gui.widgets.componentListWidget as componentList
    from gui.widgets import order_summary
    from gui.widgets.order_quantity import OrderQuantity
    from gui.widgets.distributor_selector import DistributorSelector
    from gui.widgets.supplier_info import SupplierInfo as supplier_info
    from utils import files
except:
    import widgets.componentListWidget as componentList
    from widgets import order_summary
    from widgets.order_quantity import OrderQuantity
    from widgets.distributor_selector import DistributorSelector
    from widgets.SuppliersDetailsWidget import SuppliersDetailsWidget
    from widgets.supplier_info import SupplierInfo as supplier_info

import wx
import wx.aui
from gui.OrderingBookmark import Bookmark


def cmp(a, b):
    return (a > b) - (a < b)


def add_component_price(component):
    try:
        required_quantity = component.quantity
        for distributor in component.distributors:
            # print(distributor)
            # print(component.distributors)
            for distributor_component in component.distributors[distributor]:
                order_info = distributor_component['OrderInfo']
                if required_quantity <= order_info['MinAmount']:
                    order_quantity = order_info['MinAmount']
                else:
                    mul = (required_quantity - int(order_info['MinAmount'])) / int(order_info['Multiples'])
                    order_quantity = int(order_info['MinAmount']) + int(order_info['Multiples']) * mul
                    if order_quantity < required_quantity:
                        order_quantity = order_quantity + order_info['Multiples']
                # print(component)
                distributor_component['Price'] = get_price(order_quantity,
                                                           distributor_component['PriceRanges']) * order_quantity
                distributor_component['OrderQuantity'] = order_quantity
    except TypeError:
        print(component)


def get_price(quantity, price_ranges):
    if len(price_ranges) > 0:
        for price in reversed(price_ranges):
            if quantity >= price['Amount']:
                return price['Price']
    else:
        return 0
    print(price_ranges)
    raise RuntimeError("Unable to match price range. Required quantity: " + str(quantity))


class OrderWidget(wx.aui.AuiNotebook):
    def __init__(self, parent, components, on_order_update):
        wx.aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                    wx.aui.AUI_NB_DEFAULT_STYLE)
        self.components = components
        self.on_order_update = on_order_update
        for group in self.components.keys():
            for component in self.components[group]:
                add_component_price(component)
        self.supplier_frame = {}
        self.process_components()
        self.create_bookmarks()

    def process_components(self):
        def combine(component, keys):
            #            print("Combining parameters for: " + str(component))
            result = ''
            for key in reversed(keys):
                result = str(component[key]) + '; ' + result
            return result

        columns_to_combine = {'Resistors': ['Resistance', 'Tolerance', 'Case'],
                              'Capacitors': ['Capacitance', 'Voltage', 'Dielectric Type', 'Tolerance', 'Case']}
        for component_group in self.components.keys():
            for component in self.components[component_group]:
                #                component['Price'] = 0
                #                component['Order Quantity'] = ''
                #                component['Supplier'] = 'None'
                if component_group in columns_to_combine:
                    component.combined_parameters = combine(component, columns_to_combine[component_group])



    def on_selection(self, index):
        print(index)
        for i, supplier_frame in enumerate(self.supplier_frame["Capacitors"]):
            if i == index[0]:
                supplier_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            else:
                supplier_frame.pack_forget()

    def create_bookmarks(self):
        def sort(x):
            key = {'Capacitors': 1, 'Resistors': 2, 'Others': 100}
            if x in key:
                return key[x]
            return 99

        components_group = list(self.components.keys())
        components_group.sort(key=sort)
        common_parameters_to_display = ['Quantity', 'Parameters', 'Manufacturer Part Number', 'Order Quantity',
                                        'Price', 'Supplier', 'Supplier Order Number']
        for group in components_group:
            if self.components[group]:
                if group == 'Resistors':
                    columns_to_display = common_parameters_to_display
                    validator = None  # validate_resistor
                elif group == 'Capacitors':
                    columns_to_display = common_parameters_to_display
                    validator = None  # validate_capacitor
                else:
                    keys = set(common_parameters_to_display)
                    for component in self.components[group]:
                        for key in component.parameters.keys():
                            keys.add(key)
                    columns_to_display = self.__sort_component_columns(list(keys))
                    validator = None
                columns_to_display = self.__remove_keys_if_exist(columns_to_display,
                                                                 ['Manufacturer', 'Description', 'Footprint', 'LibRef',
                                                                  'Distributors', 'Designator'])

                bookmark_layout = Bookmark(self, group, columns_to_display, self.components[group], validator,
                                           self.on_order_update)
                self.AddPage(bookmark_layout, group, False, wx.NullBitmap)

    @staticmethod
    def __sort_component_columns(component):
        def sort(x):
            keys = {'Quantity': 1, 'Comment': 2, 'Description': 3, 'Manufacturer Part Number': 4, 'Manufacturer': 5}
            if x in keys:
                return keys[x]
            return 99
        keys = component
        keys.sort(key=sort)
        return keys

    @staticmethod
    def __remove_keys_if_exist(keys, keys_to_remove):
        for key in keys_to_remove:
            if key in keys:
                keys.remove(key)
        return keys


def main(filename):
    # root = tk.Tk()
    # root.title("BOM Merger")
    # manualMerger = OrderWidget(root, filename)
    # root.mainloop()

    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

    # components = files.load_json_file(filename)
    components = {"Capacitors": [{
        "Capacitance": "1uF",
        "Case": "0805",
        "Designator": "/home/pokas/work/bommerge/tests/BOM_PartType-uHAL_DS18B20.csv: C1\n",
        "Dielectric Type": "X7R",
        "Distributors": [
            {
                "Components": [
                    {
                        "Description": "Capacitor: ceramic; 1uF; 10V; X7R; \u00b110%; 0805",
                        "Links": {
                            "Photo": "https://ce8dc832c.cloudimg.io/fit/640x480/fwk@16e51c215e1915554b0be79c406d0d5be2676b3e/_cdn_/DA/F2/B0/00/0/733101_1.jpg?mark_url=_tme-wrk_%2Ftme_new_render3d.png&mark_pos=center&mark_size=100pp",
                            "ProductInformationPage": "https://www.tme.eu/en/details/0805b105k100ct/0805-mlcc-smd-capacitors/walsin/",
                            "Thumbnail": "https://ce8dc832c.cloudimg.io/fit/100x75/webp@7d4ea33fd0784ad2da926a90658ba45b300fcb7e/_cdn_/DA/F2/B0/00/0/733101_1.jpg"
                        },
                        "OrderInfo": {
                            "MinAmount": 3000,
                            "Multiples": 3000,
                            "StockCount": 12000
                        },
                        "Parameters": {
                            "Capacitance": "1uF",
                            "Case - inch": "0805",
                            "Case - mm": "2012",
                            "Dielectric": "X7R",
                            "Manufacturer": "WALSIN",
                            "Manufacturer Part Number": "0805B105K100CT",
                            "Operating temperature": "-55...125\u00b0C",
                            "Operating voltage": "10V",
                            "Tolerance": "10",
                            "Type of capacitor": "ceramic"
                        },
                        "PriceRanges": [
                            {
                                "Amount": 3000,
                                "Price": 0.0501
                            },
                            {
                                "Amount": 9000,
                                "Price": 0.04742
                            },
                            {
                                "Amount": 15000,
                                "Price": 0.04563
                            }
                        ],
                        "Symbol": {
                            "Symbol": "0805B105K100CT",
                            "SymbolTME": "0805B105K100CT"
                        }
                    },
                    {
                        "Description": "Capacitor: ceramic; MLCC; 1uF; 10V; X7R; \u00b110%; SMD; 0805",
                        "Links": {
                            "Photo": "https://ce8dc832c.cloudimg.io/fit/640x480/fwk@16e51c215e1915554b0be79c406d0d5be2676b3e/_cdn_/DA/F2/B0/00/0/733101_1.jpg?mark_url=_tme-wrk_%2Ftme_new_render3d.png&mark_pos=center&mark_size=100pp",
                            "ProductInformationPage": "https://www.tme.eu/en/details/0805zc105kat2a/0805-mlcc-smd-capacitors/avx/",
                            "Thumbnail": "https://ce8dc832c.cloudimg.io/fit/100x75/webp@7d4ea33fd0784ad2da926a90658ba45b300fcb7e/_cdn_/DA/F2/B0/00/0/733101_1.jpg"
                        },
                        "OrderInfo": {
                            "MinAmount": 100,
                            "Multiples": 100,
                            "StockCount": 13300
                        },
                        "Parameters": {
                            "Capacitance": "1uF",
                            "Case - inch": "0805",
                            "Case - mm": "2012",
                            "Dielectric": "X7R",
                            "Kind of capacitor": "MLCC",
                            "Manufacturer": "AVX",
                            "Manufacturer Part Number": "0805ZC105KAT2A",
                            "Mounting": "SMD",
                            "Operating temperature": "-55...125\u00b0C",
                            "Operating voltage": "10V",
                            "Tolerance": "10",
                            "Type of capacitor": "ceramic"
                        },
                        "PriceRanges": [
                            {
                                "Amount": 100,
                                "Price": 0.20621
                            },
                            {
                                "Amount": 300,
                                "Price": 0.1494
                            },
                            {
                                "Amount": 1000,
                                "Price": 0.11049
                            },
                            {
                                "Amount": 4000,
                                "Price": 0.0926
                            },
                            {
                                "Amount": 12000,
                                "Price": 0.08902
                            }
                        ],
                        "Symbol": {
                            "Symbol": "0805ZC105KAT2A",
                            "SymbolTME": "0805ZC105KAT2A"
                        }
                    },
                    {
                        "Description": "Capacitor: ceramic; MLCC; 1uF; 10V; X7R; \u00b110%; SMD; 0805",
                        "Links": {
                            "Photo": "https://ce8dc832c.cloudimg.io/fit/640x480/fwk@16e51c215e1915554b0be79c406d0d5be2676b3e/_cdn_/DA/F2/B0/00/0/733101_1.jpg?mark_url=_tme-wrk_%2Ftme_new_render3d.png&mark_pos=center&mark_size=100pp",
                            "ProductInformationPage": "https://www.tme.eu/en/details/cl21b105kpfnnng/0805-mlcc-smd-capacitors/samsung/",
                            "Thumbnail": "https://ce8dc832c.cloudimg.io/fit/100x75/webp@7d4ea33fd0784ad2da926a90658ba45b300fcb7e/_cdn_/DA/F2/B0/00/0/733101_1.jpg"
                        },
                        "OrderInfo": {
                            "MinAmount": 100,
                            "Multiples": 100,
                            "StockCount": 200
                        },
                        "Parameters": {
                            "Capacitance": "1uF",
                            "Case - inch": "0805",
                            "Case - mm": "2012",
                            "Dielectric": "X7R",
                            "Kind of capacitor": "MLCC",
                            "Manufacturer": "SAMSUNG",
                            "Manufacturer Part Number": "CL21B105KPFNNNG",
                            "Mounting": "SMD",
                            "Operating temperature": "-55...125\u00b0C",
                            "Operating voltage": "10V",
                            "Tolerance": "10",
                            "Type of capacitor": "ceramic"
                        },
                        "PriceRanges": [
                            {
                                "Amount": 100,
                                "Price": 0.41914
                            },
                            {
                                "Amount": 1000,
                                "Price": 0.17311
                            },
                            {
                                "Amount": 3000,
                                "Price": 0.1002
                            },
                            {
                                "Amount": 15000,
                                "Price": 0.08499
                            }
                        ],
                        "Symbol": {
                            "Symbol": "CL21B105KPFNNNG",
                            "SymbolTME": "CL21B105KPFNNNG"
                        }
                    }
                ],
                "Name": "TME"
            },
            {
                "Components": [
                    {
                        "Description": "Capacitor MLCC 1uF \u00b110% 16V X7R -55..125\u2103 0603",
                        "Links": {
                            "Photo": "https:",
                            "ProductInformationPage": "https:",
                            "Thumbnail": "https:"
                        },
                        "OrderInfo": {
                            "MinAmount": 1,
                            "Multiples": 1,
                            "StockCount": 1000
                        },
                        "Parameters": {
                            "Capacitance": "1uF",
                            "Capacitor Type": "MLCC",
                            "Dielectric Type": "X7R",
                            "Manufacturer": "Samsung",
                            "Manufacturer Part Number": "CL10B105KO8NNNC",
                            "Storage Location": "ProductionBOX",
                            "Tolerance": "10",
                            "Voltage": "16V"
                        },
                        "PriceRanges": [
                            {
                                "Amount": 1,
                                "Price": "0.0000"
                            }
                        ],
                        "Symbol": {
                            "Name": "CL10B105KO8NNNC"
                        }
                    }
                ],
                "Name": "PartKeepr"
            }
        ],
        "Manufacturer": "",
        "Manufacturer Part Number": "",
        "Quantity": 1,
        "Tolerance": "10%",
        "Voltage": "10V",
        "validation_status": None
    },
        {
            "Capacitance": "1uF",
            "Case": "0603",
            "Designator": "/home/pokas/work/bommerge/tests/BOM_PartType-UHAL_MPL115A1.csv: C2, C3\n",
            "Dielectric Type": "X7R",
            "Distributors": [],
            "Manufacturer": "Murata",
            "Manufacturer Part Number": "GCM188R71H104KA57D",
            "Quantity": 2,
            "Tolerance": "10%",
            "Voltage": "50V",
            "validation_status": "IncorrectParameters"
        },
        {
            "Capacitance": "2.2uF",
            "Case": "0805",
            "Designator": "/home/pokas/work/bommerge/tests/BOM_PartType-UHAL_MICRO_SD_BREAKOUT.csv: C2\n",
            "Dielectric Type": "",
            "Distributors": [
                {
                    "Components": [
                        {
                            "Description": "Capacitor: ceramic; MLCC; 2.2uF; 16VDC; X7R; \u00b110%; SMD; 0805",
                            "Links": {
                                "Photo": "https://ce8dc832c.cloudimg.io/fit/640x480/fwk@16e51c215e1915554b0be79c406d0d5be2676b3e/_cdn_/DA/F2/B0/00/0/733101_1.jpg?mark_url=_tme-wrk_%2Ftme_new_render3d.png&mark_pos=center&mark_size=100pp",
                                "ProductInformationPage": "https://www.tme.eu/en/details/c0805c225k4racauto/0805-mlcc-smd-capacitors/kemet/",
                                "Thumbnail": "https://ce8dc832c.cloudimg.io/fit/100x75/webp@7d4ea33fd0784ad2da926a90658ba45b300fcb7e/_cdn_/DA/F2/B0/00/0/733101_1.jpg"
                            },
                            "OrderInfo": {
                                "MinAmount": 100,
                                "Multiples": 100,
                                "StockCount": 2500
                            },
                            "Parameters": {
                                "Manufacturer": "KEMET",
                                "Manufacturer Part Number": "C0805C225K4RACAUTO"
                            },
                            "PriceRanges": [
                                {
                                    "Amount": 100,
                                    "Price": 0.96541
                                },
                                {
                                    "Amount": 1000,
                                    "Price": 0.39856
                                },
                                {
                                    "Amount": 2500,
                                    "Price": 0.26571
                                },
                                {
                                    "Amount": 7500,
                                    "Price": 0.24781
                                }
                            ],
                            "Symbol": {
                                "Symbol": "C0805C225K4RACAUTO",
                                "SymbolTME": "C0805C225K4RACAUTO"
                            }
                        }
                    ],
                    "Name": "TME"
                }
            ],
            "Manufacturer": "Kemet",
            "Manufacturer Part Number": "C0805C225K4RACAUTO",
            "Quantity": 1,
            "Tolerance": None,
            "Voltage": "16V",
            "validation_status": "IncorrectParameters"
        }]}

    columns_to_display = ['Quantity', 'Parameters', 'Manufacturer Part Number', 'Order Quantity',
                          'Price', 'Supplier']
    group = "Capacitors"
    validator = None
    on_order_update = None
    # bookmark = Bookmark(frame, group, columns_to_display, components, validator,
    #                    on_order_update)

    order_widget = OrderWidget_(frame, components, None)

    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(order_widget, 1, wx.EXPAND, 5)
    frame.SetSizer(main_sizer)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main("orderingDialogTestData.json")
