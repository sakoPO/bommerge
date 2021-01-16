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

try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

import wx
import ntpath
from gui import orderingDialog
from utils import files
from exporters import csvExporter


def shop_selector(working_directory, filename):
    root = tk.Tk()
    ordering_widget = orderingDialog.OrderWidget(root, filename)
    root.mainloop()
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

