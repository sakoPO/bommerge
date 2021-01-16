try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

from gui.widgets.priceWidget import PriceWidget


class OrderSummary(tk.LabelFrame):
    def __init__(self, parent, shops_list):
        tk.LabelFrame.__init__(self, parent, text="Order summary")
        self.total_price_label = PriceWidget(self, 'Total price')
        self.shop_price_label = {}
        self.create_shop_label(shops_list)
        self.total_price_label.grid(column=100, row=2, padx=8, pady=2)

    def create_shop_label(self, shops):
        for i, shop in enumerate(shops):
            label = PriceWidget(self, shop)
            label.grid(column=int(i / 3), row=i % 3, padx=8, pady=2, sticky=tk.W)
            self.shop_price_label[shop] = label

    def update(self, shop, price, total_price):
        self.shop_price_label[shop].update(price)
        self.total_price_label.update(total_price)


def test():
    root = tk.Tk()
    root.title("BOM Merger")
    order = OrderSummary(root, ['TME', 'Farnel', 'Mouser', 'RS Components'])
    order.pack()
    order.update('Farnel', 10, 20)
    root.mainloop()


if __name__ == "__main__":
    test()
