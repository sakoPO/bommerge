try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class ScrolledComponentsList(ttk.Frame):
    def __init__(self, master=None, compound=tk.RIGHT, **kwargs):
        """
        :param master: master widget
        :param compound: side for the Scrollbar to be on (tk.LEFT or tk.RIGHT)
        :param listheight: height of the Listbox in items
        :param listwidth: width of the Listbox in characters
        :param kwargs: keyword arguments passed on to Listbox initializer
        """
        ttk.Frame.__init__(self, master)
        self.treeview = ttk.Treeview(self, **kwargs)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        if compound is not tk.LEFT and compound is not tk.RIGHT:
            raise ValueError("Invalid compound value passed: {0}".format(compound))
        self.treeview.tag_configure('MissingParameters', background='yellow')
        self.treeview.tag_configure('IncorrectParameters', background='red')
        self.treeview.tag_configure('PartnumberDecoderMissing', background='grey')
        self.__compound = compound
        self._grid_widgets()

    def _grid_widgets(self):
        """
        Puts the two whole widgets in the correct position depending on compound
        :return: None
        """
        scrollbar_column = 0 if self.__compound is tk.LEFT else 2
        self.treeview.grid(row=0, column=1, sticky="nswe")
        self.scrollbar.grid(row=0, column=scrollbar_column, sticky="ns")

    def addColumns(self, columns):
        self.treeview['columns'] = columns
        #self.treeview['show'] = 'headings'
        for column in columns:
            self.treeview.heading(column, text=column)
            self.treeview.column(column, width=10*len(column), anchor='center')

    def addItem(self, item, component, tag=None):
        value = []
        for key in self.treeview['columns']:
            value.append(component[key])
        if tag:
            self.treeview.insert('', 'end', text=item, values=value, tags=tag)
        else:
            self.treeview.insert('', 'end', text=item, values=value)
        
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
