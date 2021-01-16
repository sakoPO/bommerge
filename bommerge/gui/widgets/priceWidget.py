try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

class PriceWidget(ttk.Frame):
    def __init__(self, parent, shop_name):
        ttk.Frame.__init__(self, parent)
        self.shop_name_label = tk.Label(self, text=shop_name + ':')
        self.variable = tk.IntVar()
        self.price_label = tk.Label(self, textvariable=self.variable)
        self.currency_label = tk.Label(self, text='PLN')
        self.shop_name_label.pack(side=tk.LEFT)
        self.price_label.pack(side=tk.LEFT)
        self.currency_label.pack(side=tk.LEFT)

    def update(self, value):
        self.variable.set(value)