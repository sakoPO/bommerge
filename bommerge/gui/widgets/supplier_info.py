try:
    from gui.widgets import componentListWidget as componentList
    from gui.widgets.parameters import Parameters
    from gui.widgets.price_range import PriceRange
    from gui.widgets.order_info import OrderInfo as order_info_widget
    from gui.widgets.urls import Urls as urls_widget
except ImportError:
    from parameters import Parameters
    import componentListWidget as componentList
    from price_range import PriceRange
    from order_info import OrderInfo as order_info_widget
    from urls import Urls as urls_widget

try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class SupplierInfo(tk.LabelFrame):
    def __init__(self, parent, supplier_name, components, on_active_component_change):
        tk.LabelFrame.__init__(self, parent, text=supplier_name)
        self.validate = None
        self.parts = components
        self.on_change = on_active_component_change
        self.active_part = self.parts[0]
        self.active_part_index = 0

        if len(self.parts) > 1:
            self.create_component_list()
        else:
            self.parts[0]['Active'] = True

        self.create_component_details()

    def get_active_part_index(self):
        return self.active_part_index

    def add_description(self, component):
        desc = ''
        for parameter in component['Parameters']:
            desc = component['Parameters'][parameter] + '; ' + desc
        component['Description'] = desc

    def create_component_list(self):
        self.components = componentList.ScrolledComponentsList(master=self,
                                                               on_selction_change=self.on_selection_change,
                                                               on_item_double_click=self.on_item_double_click,
                                                               selectmode=tk.EXTENDED, height=4, show='headings')
        self.components.addColumns(['Manufacturer Part Number', 'Description', 'Price'])
        self.components.addDataGeter(
            {'Manufacturer Part Number': lambda x: x['Parameters']['Manufacturer Part Number']})
        self.refresh_component_list()
        self.components.pack()

    def refresh_component_list(self):
        self.components.removeAllItems()
        for i, component in enumerate(self.parts):
            if 'Description' not in component:
                self.add_description(component)
            if i == self.active_part_index:
                self.components.addItem(str(i), component, 'PartActive')
                component['Active'] = True
            else:
                self.components.addItem(str(i), component)
                component['Active'] = False

    def create_component_details(self):
        another_frame = ttk.Frame(self)
        self.parameters = Parameters(another_frame, self.active_part['Parameters'])
        self.price_order = self.create_price_order_urls(another_frame)
        self.parameters.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.price_order.pack(side=tk.LEFT)
        another_frame.pack(expand=True, fill=tk.BOTH)

    def create_price_order_urls(self, parent):
        frame = ttk.Frame(parent)
        price_order_frame = ttk.Frame(frame)
        self.price_range = PriceRange(price_order_frame, self.active_part['PriceRanges'])
        self.order_info = order_info_widget(price_order_frame, self.active_part['OrderInfo'])
        product_info_page = self.active_part['Links']['ProductInformationPage'] if 'ProductInformationPage' in \
                                                                                   self.active_part['Links'] else None
        self.urls = urls_widget(frame, product_info_page, None)

        self.price_range.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5, ipadx=5, ipady=5)
        self.order_info.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5, ipadx=5, ipady=5)
        price_order_frame.pack(anchor=tk.N)
        self.urls.pack(anchor=tk.W)
        return frame

    def on_item_double_click(self, widget):
        self.refresh_component_list()
        if self.on_change:
            self.on_change()

    def on_selection_change(self):
        self.active_part_index = self.components.getSelectedIndices()[0]
        self.active_part = self.parts[self.components.getSelectedIndices()[0]]
        self.order_info.update(self.active_part['OrderInfo'])
        self.price_range.update(self.active_part['PriceRanges'])
        self.parameters.update(self.active_part['Parameters'])


def main():
    root = tk.Tk()
    root.title("BOM Merger")

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
    order = SupplierInfo(root, "test supplier", Components, None)
    order.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
