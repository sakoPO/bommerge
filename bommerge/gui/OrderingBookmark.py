try:
    import gui.widgets.componentListWidget as componentList
    from gui.widgets import order_summary
    from gui.widgets.order_quantity import OrderQuantity
    from gui.widgets.distributor_selector import DistributorSelector
    from gui.widgets.SuppliersDetailsWidget import SuppliersDetailsWidget
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


class ComponentGroup(wx.BoxSizer):
    def __init__(self, parent, name, columns, components, validator_function=None, on_selection=None):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.parent = parent
        self.name = name
        self.columns_resized = False
        self.components = components
        self.validate = validator_function
        self.create_gui(columns)
        self.refresh_widget()

        #        if self.name == 'Capacitors':
        #            self.value_key = 'Capacitance'
        # from partnameDecoder import capacitors as capacitorResolver
        #            self.resolver = None#capacitorResolver
        #        elif self.name == 'Resistors':
        #            self.value_key = 'Resistance'
        #            from partnameDecoder import resistors as resistorResolver
        #            self.resolver = resistorResolver
        #        else:
        self.value_key = 'Comment'
        self.resolver = None
        self.on_selection_change = on_selection

    def create_gui(self, columns):
        def on_selection_change(index):
            if self.on_selection_change:
                self.on_selection_change(self.widget.get_selected_items())

        self.widget = componentList.ScrolledComponentsList_v3(parent=self.parent, columns=columns,
                                                              on_selection_change=on_selection_change,
                                                              on_item_double_click=self.on_item_double_click)
        self.widget.add_data_geter({'Parameters': lambda
            component: component.combined_parameters if component.combined_parameters is not None else "",
                                    'Price': lambda component: '%.4f' % component.order_info.price,
                                    'Supplier': lambda component: component.order_info.distributor_name,
                                    'Order Quantity': lambda component: str(component.order_info.quantity),
                                    'Supplier Order Number': lambda
                                        component: component.order_info.distributor_order_number if component.order_info.distributor_order_number is not None else ""})

        self.Add(self.widget, 1, wx.EXPAND, 5)

    def sort(self):
        if self.name == 'Capacitors':
            self.components.sort(key=lambda x: capacitor.convertCapacitanceToFarads(x['Capacitance']))
        elif self.name == 'Resistors':
            self.components.sort(key=lambda x: resistor.convertResistanceToOhms(x['Resistance']))
        else:
            self.components.sort()

    def refresh_widget(self):
        self.widget.remove_all_items()
        self.widget.add_items(self.components, None)
        if not self.columns_resized:
            self.columns_resized = True
            for i in range(self.widget.GetColumnCount()):
                self.widget.SetColumnWidth(i, wx.LIST_AUTOSIZE)

        # for i, component in enumerate(self.components):
        #     if self.validate:
        #         component['validation_status'] = self.validate(component)
        #     if 'validation_status' in component:
        #         self.widget.addItem(str(i), component, component['validation_status'])
        #     else:
        #         self.widget.addItem(str(i), component)

    def remove_components_by_indices(self, indices_list):
        indices_list.sort(reverse=True)
        for index in indices_list:
            tmp = self.components.pop(index)
            print("Removing component " + str(tmp[self.value_key]) + ', With index: ' + str(index))

    def on_item_double_click(self, event):
        item = self.widget.getSelectedIndices()
        print("you clicked on: ", item)
        component = self.components[item[0]]
        if 'Manufacturer Part Number' in component:
            resolved_parameters = self.resolver.resolve(component['Manufacturer Part Number'])
        partDetailDialog.PartDetailDialog(self.parent, component, resolved_parameters)


class Bookmark(wx.SplitterWindow):
    def __init__(self, parent, group, columns_to_display, components, validator, on_order_update):
        wx.SplitterWindow.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D)
        self.components = components
        self.on_order_update = on_order_update
        self.active_component_index = 0

        self.components_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.components_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.components_panel.SetSizer(self.components_panel_sizer)
        self.supplier_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.supplier_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.supplier_panel.SetSizer(self.supplier_panel_sizer)
        self.component_frame = ComponentGroup(self.components_panel, group, columns_to_display, components, validator,
                                              self.on_selection)
        self.components_panel_sizer.Add(self.component_frame, 1, wx.ALL | wx.EXPAND, 5)

        self.supplier_frame = []
        for component in components:
            suppliersWidget = SuppliersDetailsWidget(self.supplier_panel, component.distributors,
                                                     self.on_component_order_change)
            suppliersWidget.Show(False)
            self.supplier_panel_sizer.Add(suppliersWidget, 1, wx.EXPAND, 5)
            self.supplier_frame.append(suppliersWidget)

        self.supplier_frame[0].Show()
        self.SplitVertically(self.components_panel, self.supplier_panel, 700)

    def on_selection(self, index):
        # print(index)
        self.active_component_index = index[0]
        for i, supplier_frame in enumerate(self.supplier_frame):
            if i == index[0]:
                supplier_frame.Show(True)
                self.supplier_panel_sizer.Layout()
            else:
                supplier_frame.Show(False)

    def on_component_order_change(self, distributor_name, quantity, distributor_part_index):
        component = self.components[self.active_component_index]
        component.update_order_info(quantity, distributor_name, distributor_part_index)
        self.component_frame.refresh_widget()
        if self.on_order_update:
            self.on_order_update()


def main():
    components = [{
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
        }]

    app = wx.App()
    frame = wx.Frame(None, id=wx.ID_ANY, title=u"test", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                     style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

    columns_to_display = ['Quantity', 'Parameters', 'Manufacturer Part Number', 'Order Quantity',
                          'Price', 'Supplier']
    group = "Capacitors"
    validator = None
    on_order_update = None
    bookmark = Bookmark(frame, group, columns_to_display, components, validator,
                        on_order_update)

    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(bookmark, 1, wx.EXPAND, 5)
    frame.SetSizer(main_sizer)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
