try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class order_quantity(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.order_quantity_label = tk.Label(self, text='Order Quantity: ')
        self.quantity_entry = tk.Entry(self)
        self.order_quantity_label.grid(row=0, column=0)       
        self.quantity_entry.grid(row=0, column=1)

