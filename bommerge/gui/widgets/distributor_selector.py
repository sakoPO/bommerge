try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

class distributor_selector(tk.LabelFrame):
    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text="Distributor selection")
        
        self.active_distributor = tk.IntVar()
        self.active_distributor = 1
        
        self.distributor_none = tk.Radiobutton(self, text='None', variable=self.active_distributor, value=1)
        self.distributor_part_keeper = tk.Radiobutton(self, text='PartKeeper', variable=self.active_distributor, value=2)
        self.distributor_tme = tk.Radiobutton(self, text='TME', variable=self.active_distributor, value=3)
        self.distributor_rs = tk.Radiobutton(self, text='RS Components', variable=self.active_distributor, value=3)
        self.distributor_farnel = tk.Radiobutton(self, text='Farnel', variable=self.active_distributor, value=3)
        self.distributor_mouser = tk.Radiobutton(self, text='Mouser', variable=self.active_distributor, value=3)
                
        self.distributor_none.grid(column=0, row=0, sticky=tk.W)
        self.distributor_part_keeper.grid(column=0, row=1, sticky=tk.W)
        self.distributor_tme.grid(column=0, row=2, sticky=tk.W)
        self.distributor_rs.grid(column=1, row=0, sticky=tk.W)
        self.distributor_farnel.grid(column=1, row=1, sticky=tk.W)
        self.distributor_mouser.grid(column=1, row=2, sticky=tk.W)


