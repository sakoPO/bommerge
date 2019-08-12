try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class ScrolledComponentsList(ttk.Frame):
    def __init__(self, master, on_selction_change, on_item_double_click, compound=tk.RIGHT, **kwargs):
        """
        :param master: master widget
        :param compound: side for the Scrollbar to be on (tk.LEFT or tk.RIGHT)
        :param listheight: height of the Listbox in items
        :param listwidth: width of the Listbox in characters
        :param kwargs: keyword arguments passed on to Listbox initializer
        """
        ttk.Frame.__init__(self, master)
        self.dataGeter = {}
        self.treeview = ttk.Treeview(self, **kwargs)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        if compound is not tk.LEFT and compound is not tk.RIGHT:
            raise ValueError("Invalid compound value passed: {0}".format(compound))
        self.treeview.tag_configure('MissingParameters', background='yellow')
        self.treeview.tag_configure('IncorrectParameters', background='red')
        self.treeview.tag_configure('PartnumberDecoderMissing', background='grey')
        self.treeview.tag_configure('PartActive', background='green')
        self.on_selction_change = on_selction_change
        self.treeview.bind('<ButtonRelease-1>', self._on_item_selected)
        if on_item_double_click:
            self.treeview.bind('<Double-1>', on_item_double_click)
        self.__compound = compound
        self._grid_widgets()

    def _on_item_selected(self, event):
        if self.on_selction_change:
            self.on_selction_change()

    def _grid_widgets(self):
        self.treeview.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    def addDataGeter(self, geter):
        self.dataGeter = geter

    def addColumns(self, columns):
        max_width = {'Quantity': 10*len('Quantity')}
        self.treeview['columns'] = columns
#        self.treeview['show'] = 'headings'
        for column in columns:
            self.treeview.heading(column, text=column)
            if column in max_width:
                self.treeview.column(column, minwidth=10*len(column), width=max_width[column], anchor='center', stretch=tk.NO)
            else:
                self.treeview.column(column, minwidth=10*len(column), anchor='center', stretch=tk.YES)

    def addItem(self, item, component, tag=None):
        try:
            value = []
            for key in self.treeview['columns']:
                if key in self.dataGeter:
                    value.append(self.dataGeter[key](component))
                else:
                    if key in component:
                        value.append(component[key])
                    else:
                        value.append("")
            if tag:
                self.treeview.insert('', 'end', text=item, values=value, tags=tag)
            else:
                self.treeview.insert('', 'end', text=item, values=value)
        except:
            print("item " + str(item) + " Component " + str(component))
            raise
        
    def removeAllItems(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        
    def getSelectedIndices(self):
        indices = []
        for item in self.treeview.selection():
            indices.append(int(self.treeview.item(item,"text")))
        return indices

    def getSelected(self):
        return self.treeview.selection()

    def getDisplayedFieldsNames(self):    
        return self.treeview['columns']
