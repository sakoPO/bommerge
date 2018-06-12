try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    
class order_info(tk.LabelFrame):
    def __init__(self, parent, order_info_data):
        tk.LabelFrame.__init__(self, parent, text="Order information")        
        self.min_order_label = tk.Label(self, text='Minimal Order:')
        self.mul_order_label =  tk.Label(self, text='Multiplicity:')
        self.stock_lavel = tk.Label(self, text='Stock level:')
        self.min_order_label.grid(row=0, column=0)       
        self.mul_order_label.grid(row=1, column=0)
        self.stock_lavel.grid(row=2, column=0)
        
        self.min_order = tk.StringVar()
        self.mul_order = tk.StringVar()
        self.stock_lavel = tk.StringVar()       
        
        self.min_order_value = tk.Label(self, textvariable=self.min_order)
        self.mul_order_value =  tk.Label(self, textvariable=self.mul_order)
        self.stock_lavel_value = tk.Label(self, textvariable=self.stock_lavel)
        self.min_order_value.grid(row=0, column=1)       
        self.mul_order_value.grid(row=1, column=1)
        self.stock_lavel_value.grid(row=2, column=1)
        self.update(order_info_data)

    def update(self, order_info_data):
        self.min_order.set(str(order_info_data['MinAmount']))
        self.mul_order.set(str(order_info_data['Mul']))
        self.stock_lavel.set(str(order_info_data['Stock']))

