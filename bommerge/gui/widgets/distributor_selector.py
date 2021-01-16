try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class DistributorSelector(tk.LabelFrame):
    def __init__(self, parent, on_distributor_change = None):
        tk.LabelFrame.__init__(self, parent, text="Distributor selection")
        
        self.on_distributor_change = on_distributor_change
        self.active_distributor = tk.IntVar()
        self.active_distributor.set(1)

        self.distributor = {}        
        self.distributor['None'] = tk.Radiobutton(self, text='None', variable=self.active_distributor, value=1, command=self._on_selection)
        self.distributor['PartKeepr'] = tk.Radiobutton(self, text='PartKeepr', variable=self.active_distributor, value=2, command=self._on_selection)
        self.distributor['TME'] = tk.Radiobutton(self, text='TME', variable=self.active_distributor, value=3, command=self._on_selection)
        self.distributor['RS Components'] = tk.Radiobutton(self, text='RS Components', variable=self.active_distributor, value=4, command=self._on_selection)
        self.distributor['Farnel'] = tk.Radiobutton(self, text='Farnel', variable=self.active_distributor, value=5, command=self._on_selection)
        self.distributor['Mouser'] = tk.Radiobutton(self, text='Mouser', variable=self.active_distributor, value=6, command=self._on_selection)
                
        self.distributor['None'].grid(column=0, row=0, sticky=tk.W)
        self.distributor['PartKeepr'].grid(column=0, row=1, sticky=tk.W)
        self.distributor['TME'].grid(column=0, row=2, sticky=tk.W)
        self.distributor['RS Components'].grid(column=1, row=0, sticky=tk.W)
        self.distributor['Farnel'].grid(column=1, row=1, sticky=tk.W)
        self.distributor['Mouser'].grid(column=1, row=2, sticky=tk.W)

    def activate(self, distributors):
        for distributor in self.distributor.keys():
            self.distributor[distributor]['state'] = tk.NORMAL if distributor in distributors else tk.DISABLED
           

    def _on_selection(self):
        print("selected: " + str(self.active_distributor.get()))
        if self.on_distributor_change:
            self.on_distributor_change(self.get())

    def get(self):
        val_to_str = ['None', 'PartKeepr', 'TME', 'RS Components', 'Farnel', 'Mouser']
        return val_to_str[self.active_distributor.get() - 1]


def test():
    root = tk.Tk()
    root.title("BOM Merger")
    order = DistributorSelector(root, ['TME', 'Farnel', 'Mouser', 'RS Components'])
    order.pack()
    root.mainloop()


if __name__ == "__main__":
    test()
