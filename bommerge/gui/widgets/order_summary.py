try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class price_widget(ttk.Frame):
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


class order_summary(tk.LabelFrame):
    def __init__(self, parent, shops_list):
        tk.LabelFrame.__init__(self, parent, text="Order summary")        
        self.total_price_label = price_widget(self, 'Total price')
        self.shop_price_label = {}
        self.create_shop_label(shops_list)
        self.total_price_label.grid(column=100,row=2,padx=8, pady=2)

        
    def create_shop_label(self, shops):
        for i, shop in enumerate(shops):
            label = price_widget(self, shop)
            label.grid(column=int(i/3), row=i%3, padx=8, pady=2,sticky=tk.W)
            self.shop_price_label[shop] = label
            

    def update(self, shop, price, total_price):
        self.shop_price_label[shop].update(price)
        self.total_price_label.update(total_price)


def main():
    root = tk.Tk()
    root.title("BOM Merger")
    order = order_summary(root, ['TME', 'Farnel', 'Mouser', 'RS Components'])
    order.pack()
    order.update('Farnel',10, 20)
    root.mainloop()
    
if __name__ == "__main__":
    main()
