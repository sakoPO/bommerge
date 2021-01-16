try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

class range_widget:
    def __init__(self, parent):
        self.amount_variable = tk.StringVar()
        self.price_variable = tk.StringVar()
        self.amount_label = tk.Label(parent, textvariable=self.amount_variable)
        self.price_label = tk.Label(parent, textvariable=self.price_variable)


    def update(self, amount, price):
        self.amount_variable.set(str(amount))
        self.price_variable.set(str(price))


    def grid(self, **kwargs):
        self.amount_label.grid(kwargs, column=0)
        self.price_label.grid(kwargs, column=1)

    def grid_forget(self):
        self.amount_label.grid_forget()
        self.price_label.grid_forget()

class PriceRange(tk.LabelFrame):
    def __init__(self, parent, ranges):
        tk.LabelFrame.__init__(self, parent, text="Price Range")
        self.amount_label = tk.Label(self, text='Amount')
        self.price_label =  tk.Label(self, text='Price')
        self.amount_label.grid(row=0, column=0)       
        self.price_label.grid(row=0, column=1)
        self.widgets = []
        self.update(ranges)       


    def update(self, ranges):
        for i in range(len(ranges) - len(self.widgets)):
            self.widgets.append(range_widget(self)) 
        
        for i, price_step in enumerate(ranges):
            self.widgets[i].update(price_step['Amount'], price_step['Price'])
        
        for i, widget in enumerate(self.widgets):
            if i < len(ranges):
                widget.grid(row=i+1)
            else:
                widget.grid_forget()


def test():
    root = tk.Tk()
    root.title("BOM Merger")
    PriceRanges= [
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
        }]
    order = PriceRange(root, PriceRanges)
    order.pack()
    root.mainloop()


if __name__ == "__main__":
    test()

