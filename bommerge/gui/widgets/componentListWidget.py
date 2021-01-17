try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

import wx


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


class ScrolledComponentsList_v2(wx.ListView):
    def __init__(self, parent, on_selction_change, on_item_double_click, compound=tk.RIGHT, **kwargs):
        """
        :param master: master widget
        :param compound: side for the Scrollbar to be on (tk.LEFT or tk.RIGHT)
        :param listheight: height of the Listbox in items
        :param listwidth: width of the Listbox in characters
        :param kwargs: keyword arguments passed on to Listbox initializer
        """
        wx.ListView.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        self.dataGeter = {}
        #self.treeview = ttk.Treeview(self, **kwargs)
        #self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        #self.treeview.configure(yscrollcommand=self.scrollbar.set)
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
        max_width = {'Quantity': 10 * len('Quantity')}
        #self.treeview['columns'] = columns
        #        self.treeview['show'] = 'headings'
        for column in columns:
            self.AppendColumn(column)
            #self.treeview.heading(column, text=column)
            #if column in max_width:
            #    self.treeview.column(column, minwidth=10 * len(column), width=max_width[column], anchor='center',
            #                         stretch=tk.NO)
            #else:
            #    self.treeview.column(column, minwidth=10 * len(column), anchor='center', stretch=tk.YES)

    def addItem(self, item, component, tag=None):
        try:
            self.SetItem(0, 1, "100uf")
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
                #self.treeview.insert('', 'end', text=item, values=value, tags=tag)
                self.InsertItem(0, value)
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
            indices.append(int(self.treeview.item(item, "text")))
        return indices

    def getSelected(self):
        return self.treeview.selection()

    def getDisplayedFieldsNames(self):
        return self.treeview['columns']


class ScrolledComponentsList_v3(wx.ListView):
    def __init__(self, parent, columns, on_selection_change, on_item_double_click, flags=0):
        wx.ListView.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT | flags)
        self.parent = parent
        self.on_selection_change = on_selection_change
        self.on_double_click = on_item_double_click
        self.data_geter = {}
        self.columns = columns
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.__on_double_click, id=self.GetId())
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.__on_selection, id=self.GetId())

        for column in columns:
            self.AppendColumn(column)

    def add_items(self, components, validation_status):
        for index, component in enumerate(components):
            item_number = self.GetItemCount()
            self.InsertItem(item_number, item_number)
            for i, column in enumerate(self.columns):
                if column in self.data_geter:
                    self.SetItem(item_number, i, self.data_geter[column](component))
                elif column in component:
                    self.SetItem(item_number, i, str(component[column]))

            if validation_status is None or validation_status[index] is None:
                self.SetItemBackgroundColour(item_number, wx.WHITE)
            elif validation_status[index] == "IncorrectParameters":
                self.SetItemBackgroundColour(item_number, wx.YELLOW)
            elif validation_status[index] == "IncorrectParameters":
                self.SetItemBackgroundColour(item_number, wx.RED)

    def add_data_geter(self, getter):
        self.data_geter = getter

    def remove_all_items(self):
        self.DeleteAllItems()

    def get_selected_items(self):
        selected_items = []
        item = -1
        while True:
            item = self.GetNextItem(item, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if item == -1:
                break
            selected_items.append(item)
        return selected_items

    def __on_double_click(self, event):
        self.on_double_click(event.GetIndex())

    def __on_selection(self, event):
        self.on_selection_change(event.GetIndex())
