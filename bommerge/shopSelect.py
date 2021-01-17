try:
    from components import resistor
    from components import capacitor
    from components import voltage
    from components import tolerance
except:
    from bommerge.components import resistor
    from bommerge.components import capacitor
    from bommerge.components import voltage
    from bommerge.components import tolerance

from gui.orderingDialog import OrderWidget
from gui.widgets.order_summary import OrderSummary
import wx
import ntpath
from gui import orderingDialog
from utils import files
from exporters import csvExporter
from Component import *


def decode_component(component):
    # print(component)
    parameters = component.copy()
    parameters.pop("Quantity")
    parameters.pop("Distributors")
    parameters.pop("validation_status", False)

    distributors = {}
    for distributor in component["Distributors"]:
        distributors[distributor["Name"]] = distributor["Components"]
    return Component(parameters, component["Quantity"], distributors)


def process_components(components):
    components_group = {}
    for group in components:
        decoded_components = []
        for part in components[group]:
            decoded_components.append(decode_component(part))
        components_group[group] = decoded_components
    return components_group


class ShopFrame(wx.Frame):
    def __init__(self, parent, filename):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Bommerge distributor selector", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.components = process_components(files.load_json_file(filename))
        self.order = {}
        self.result = None
        self.notebook = OrderWidget(self, self.components, self.on_order_update)
        self.order_summary = OrderSummary(self, ['TME', 'Farnel', 'Mouser', 'RS Components', 'PartKeepr'])
        self.cancel_button = wx.Button(self, id=wx.ID_ANY, label='Cancel')
        self.done_button = wx.Button(self, id=wx.ID_ANY, label='Done')

        # layout
        self.buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons_sizer.Add(self.cancel_button)
        self.buttons_sizer.Add(self.done_button)

        self.bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bottom_sizer.Add(self.order_summary, 1, wx.ALL | wx.EXPAND, 5)
        self.bottom_sizer.Add(self.buttons_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(self.bottom_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.main_sizer)

    def cancel(self):
        pass

    def done(self):
        self.update_result()

    def calculate_order_price(self):
        new_order = {}
        for group in self.components.keys():
            for component in self.components[group]:
                supplier = component.order_info.distributor_name
                if supplier in new_order:
                    new_order[supplier] = new_order[supplier] + component.order_info.price
                else:
                    new_order[supplier] = component.order_info.price
        for key in new_order.keys():
            self.order[key] = new_order[key]
        for key in self.order.keys():
            if key not in new_order.keys():
                self.order[key] = 0

    def calculate_total_price(self):
        total_price = 0
        for key in self.order.keys():
            total_price = total_price + self.order[key]
        return total_price

    def on_order_update(self):
        self.calculate_order_price()
        total_price = self.calculate_total_price()
        for shop in self.order.keys():
            if shop not in [None, "None"]:
                self.order_summary.update(shop, self.order[shop], total_price)

    def update_result(self):
        def get_shop_url(component):
            for distributor in component['Distributors']:
                if distributor['Name'] == component['Supplier']:
                    for component in distributor['Components']:
                        if 'Active' in component and component['Active'] == True:
                            return component['Links']['ProductInformationPage']

        def get_manufacturer_part_number(component):
            if 'Manufacturer Part Number' in component:
                return component['Manufacturer Part Number']
            return ''

        def get_shop_part_number(component):
            try:
                for distributor in component['Distributors']:
                    if distributor['Name'] == component['Supplier']:
                        for component in distributor['Components']:
                            if 'Active' in component and component['Active'] == True:
                                return component['Symbol']['SymbolTME']
            except KeyError:
                print(component)
                return "Error"

        self.result = {}
        for group in self.components.keys():
            for component in self.components[group]:
                supplier = component['Supplier']
                part = {'Manufacturer Part Number': get_manufacturer_part_number(component),
                        'Quantity': component['Order Quantity'], 'Shop URL': get_shop_url(component),
                        'Shop Part Number': get_shop_part_number(component)}
                if supplier in self.result:
                    self.result[supplier].append(part)
                else:
                    self.result[supplier] = [part]


def shop_selector(working_directory, filename):
    app = wx.App()
    ordering_widget = ShopFrame(None, filename)
    ordering_widget.Show()
    app.MainLoop()
    filename = working_directory + 'tmp/order.json'
    files.save_json_file(filename, ordering_widget.components)
    if ordering_widget.result:
        for supplier in ordering_widget.result.keys():
            csvExporter.save_list(ordering_widget.result[supplier],
                                  working_directory + '/' + supplier + '_human_readable.csv')
            order_list = []
            for component in ordering_widget.result[supplier]:
                order_list.append({'Part number': component['Shop Part Number'], 'Quantity': component['Quantity']})
            csvExporter.save_list(order_list, working_directory + '/' + supplier + '.csv', write_header=False)


if __name__ == "__main__":
    app = wx.App()
    # Create open file dialog
    openFileDialog = wx.FileDialog(None, "Open", "", "",
                                   "merged file (*.json)|*.json",
                                   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    result = openFileDialog.ShowModal()
    if result == wx.ID_OK:
        path = openFileDialog.GetPath()
        print(path)
        shop_selector(ntpath.basename(path), path)
    openFileDialog.Destroy()
