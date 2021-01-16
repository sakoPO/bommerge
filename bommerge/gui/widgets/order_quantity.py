try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class OrderQuantity(ttk.Frame):
    def __init__(self, parent, on_quantity_change):
        ttk.Frame.__init__(self, parent)
        self.quantity = tk.StringVar()
        if on_quantity_change:
            self.quantity.trace('w', lambda name, index, mode, quantity=self.quantity: on_quantity_change(quantity))
        self.order_quantity_label = tk.Label(self, text='Order Quantity: ')
        self.quantity_entry = tk.Entry(self, textvariable=self.quantity)
        self.order_quantity_label.grid(row=0, column=0)       
        self.quantity_entry.grid(row=0, column=1)

    def get(self):
        try:
            return int(self.quantity.get())
        except:
            return None

    def make_invalid(self):
        self.quantity_entry['bg'] = 'red'

    def make_valid(self):
        self.quantity_entry['bg'] = 'white'


def test():
    root = tk.Tk()
    root.title("BOM Merger")
    order = OrderQuantity(root, None)

    order.pack()
    root.mainloop()


if __name__ == "__main__":
    test()
