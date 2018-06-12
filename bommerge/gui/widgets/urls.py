try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

class urls(ttk.Frame):
    def __init__(self, parent, partinfo_url, datasheat_url):
        ttk.Frame.__init__(self, parent)
        self.shop_label = tk.Label(self, text=r"Component page", fg="blue", cursor="hand2")        
        self.shop_label.bind("<Button-1>", self.open_partinfo_page)
        self.datasheat_label = tk.Label(self, text=r"Datasheat", fg="blue", cursor="hand2")        
        self.datasheat_label.bind("<Button-1>", self.open_datasheat)
        self.shop_label.pack(side=tk.LEFT, padx=10)
        self.datasheat_label.pack(side=tk.LEFT, padx=10)
        self.update(partinfo_url, datasheat_url)

    def update(self, partinfo_url, datasheat_url):
        self.partinfo_url = partinfo_url
        self.datasheat_url = datasheat_url
        if self.partinfo_url:
            self.shop_label['fg'] = "blue"
        else:
            self.shop_label['fg'] = "grey"

        if self.datasheat_url:
            self.datasheat_label['fg'] = "blue"
        else:
            self.datasheat_label['fg'] = "grey"

    def open_partinfo_page(self, event):
        import webbrowser
        webbrowser.open_new(self.partinfo_url)


    def open_datasheat(self, event):
        import webbrowser
        webbrowser.open_new(self.datasheat_url)
