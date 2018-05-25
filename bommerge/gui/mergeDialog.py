try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    
mergedComponent = {}   

class MergeDialog(tk.Toplevel):
    def __init__(self, parent, columns, components):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.title("Manual merging")
        self.parent = parent
        self.result = None
    
        self._createComponentsTable(columns, components)
        
        merged = self.mergeFields(components)
        mergeFields = self._createMergeFields(columns, merged)
        self._createButtons(mergeFields, merged)
        
        self.protocol("WM_DELETE_WINDOW", self.cancel)        
        self.wait_window(self)

    @staticmethod
    def sumQuantity(components):
        quantity = 0
        for component in components:
            quantity = quantity + int(component['Quantity'])
        return quantity
        
    @staticmethod
    def mergeDesignator(components):
        designator = ''
        for component in components:
            designator = designator + component['Designator']
        return designator

    def mergeFields(self, components):    
        def replaceNone(fieldValue):
            if fieldValue:
                return fieldValue
            return ''
    
        merged = {}
        merged['Quantity'] = self.sumQuantity(components)
        merged['Designator'] = self.mergeDesignator(components)
        
        for component in components:
            for field in component.keys():
                if field in ['Quantity', 'Designator']:
                    continue
                if field not in merged:
                    merged[field] = set()

                merged[field].add(replaceNone(component[field]))
        return merged
                        
    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()
        
    @staticmethod
    def merge(combos, merged):        
        for field in merged.keys():
            if field in ['Quantity', 'Designator']:
                mergedComponent[field] = merged[field]
            else:
                mergedComponent[field] = combos[field].get()
        return mergedComponent


    def _createComponentsTable(self, columns, components):
        parent = ttk.Frame(self)
        r = 0
        for c, column in enumerate(columns):
            l = tk.Label(parent, text=column)
            l.grid(row=0, column=c)
            for r, component in enumerate(components):       
                e = tk.Entry(parent, disabledbackground='white', disabledforeground='black')
                if component[column]:
                    e.insert(10, component[column])
                e.grid(row=r+1, column=c)
                e.config(state=tk.DISABLED)
        parent.pack()        
            
    def _createMergeFields(self, columns, component):
        def createTextWidget(parent, text):
            textWidget = tk.Text(parent, width=50, height=10)
            textWidget.insert(tk.INSERT, text)        
            return textWidget
            
        def createEntryWidget(parent, value):
            entry = tk.Entry(parent, disabledbackground='white', disabledforeground='black')
            if type(value) is set:
                entry.insert(10, list(component[column])[0])
            else:    
                entry.insert(10, value)
            return entry
        
        parent = ttk.Frame(self)
        l = tk.Label(parent, text='Merged')
        l.grid(row=0, column=0)
        
        mergeFields = {}
        for c, column in enumerate(columns):
            label = tk.Label(parent, text=column)
            label.grid(row=1, column=c) 

            if column == 'Designator':
                widget = createTextWidget(parent, text=component['Designator'])
                widget.config(state=tk.DISABLED)
            elif column == 'Quantity':
                widget = createEntryWidget(parent, component[column])
                widget.config(state=tk.DISABLED)
            elif len(component[column]) == 1:
                widget = createEntryWidget(parent, component[column])
            else:
                widget = ttk.Combobox(parent)
                widget['values'] = list(component[column])                       
            widget.grid(row=2, column=c, sticky=tk.N)
            mergeFields[column] = widget
            
        parent.pack()        
        return mergeFields
                
    def _createButtons(self, combos, merged):
        parent = ttk.Frame(self)
        def doMerge():
            self.result = self.merge(combos, merged)
            self.withdraw()
            self.update_idletasks()
            self.cancel()

        button = tk.Button(parent, text='Done', width=10, command=doMerge)
        button.grid(row=0, column=0) 
        
        button = tk.Button(parent, text='Cancel', width=10, command=self.cancel)
        button.grid(row=0, column=1)
        parent.pack(side=tk.RIGHT) 
        






  
    
   
