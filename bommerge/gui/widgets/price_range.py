try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

class price_range(tk.LabelFrame):
    def __init__(self, parent, ranges):
        tk.LabelFrame.__init__(self, parent, text="Price Range")
        self.amount_label = tk.Label(self, text='Amount')
        self.price_label =  tk.Label(self, text='Price')
        self.amount_label.grid(row=0, column=0)       
        self.price_label.grid(row=0, column=1)
        self.amount = []
        self.price = []
        for i, range in enumerate(ranges):
            self.amount.append(tk.Label(self, text=str(range['Amount'])))
            self.price.append(tk.Label(self, text=str(range['Price'])))
            self.amount[i].grid(column=0, row=i+1)
            self.price[i].grid(column=1, row=i+1)

