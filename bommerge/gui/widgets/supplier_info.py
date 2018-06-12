import componentListWidget as componentList
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    
    
class parameters(tk.LabelFrame):
    def __init__(self, parent, parameters):
        tk.LabelFrame.__init__(self, parent, text="Parameters")
        self.variable = []
        self.label = []
        self.update(parameters)


    def _add_parameter(self):
        self.variable.append(tk.StringVar())
        self.label.append(tk.Label(self, textvariable=self.variable[-1]))


    def update(self, parameters):
        for i in range(len(parameters) - len(self.label)):
            self._add_parameter()
            
        for i, parameter in enumerate(parameters):
            self.variable[i].set(str(parameter) + ': ' + str(parameters[parameter]))

        for i, label in enumerate(self.label):
            if i < len(parameters):
                label.grid(row=i, sticky=tk.W, padx=10)
            else:
                label.grid_forget()


class supplier_info(tk.LabelFrame):
    ''' 
    components is a list of dictionarys, each dictionary contain information about one component:
    [
      {
        'Manufacturer Part Number': <>,
        'OrderInfo': {'MinAmount': <intiger, minimal amount that can be ordered>, 'Mul': <integer, order multiplication>, 'Stock': <integer, current stock level>},
        'PriceRanges': 
          [
            {'Amount': <integer>, 'Price': <flaot>},
            {'Amount': 20, 'Price': 0.1620},
            ...
          ]
        'Parameters': {<ParameterName>: <ParameterValue>, ...}
        'PartinfoUrl': ''
        'DatasheatUrl': ''
      }
    ]
    '''    
    def __init__(self, parent, supplier_name, components, on_active_component_change):
        tk.LabelFrame.__init__(self, parent, text=supplier_name)
        self.validate = None
        self.parts = components
        self.on_change = on_active_component_change
        self.active_part = self.parts[0]
        self.active_part_index = 0

        if len(self.parts) > 1:
            self.create_component_list()

        self.create_component_details()


    def get_active_part_index(self):
        return self.active_part_index


    def add_description(self, component):
        desc = ''
        for parameter in component['Parameters']:
            desc = component['Parameters'][parameter] + '; ' + desc
        component['Description'] = desc

    def create_component_list(self):
        self.components = componentList.ScrolledComponentsList(master=self,
                                                           on_selction_change=self.on_selection_change,
                                                           on_item_double_click=self.on_item_double_click,
                                                           selectmode=tk.EXTENDED, height=4, show = 'headings')
        self.components.addColumns(['Manufacturer Part Number', 'Description', 'Price'])
        self.refresh_component_list()
        self.components.pack()


    def refresh_component_list(self):
        self.components.removeAllItems()
        for i, component in enumerate(self.parts):
            if 'Description' not in component:
                self.add_description(component)
            if i == self.active_part_index:
                self.components.addItem(str(i), component, 'PartActive')
            else:
                self.components.addItem(str(i), component)


    def create_component_details(self):
        another_frame = ttk.Frame(self)
        self.parameters = parameters(another_frame, self.active_part['Parameters'])
        self.price_order = self.create_price_order_urls(another_frame)
        self.parameters.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.price_order.pack(side=tk.LEFT)
        another_frame.pack(expand=True, fill=tk.BOTH)


    def create_price_order_urls(self, parent):
        from widgets.price_range import price_range
        from widgets.order_info import order_info as order_info_widget
        from widgets.urls import urls as urls_widget
      
        frame = ttk.Frame(parent)
        price_order_frame = ttk.Frame(frame)
        self.price_range = price_range(price_order_frame, self.active_part['PriceRanges'])
        self.order_info = order_info_widget(price_order_frame, self.active_part['OrderInfo'])
        self.urls = urls_widget(frame, None, None)
        
        self.price_range.pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)  
        self.order_info.pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)        
        price_order_frame.pack()
        self.urls.pack(anchor=tk.W)
        return frame

    def on_item_double_click(self, widget):
        self.refresh_component_list()
        if self.on_change:
            self.on_change()
    
    def on_selection_change(self):
        self.active_part_index = self.components.getSelectedIndices()[0]
        self.active_part = self.parts[self.components.getSelectedIndices()[0]]
        self.order_info.update(self.active_part['OrderInfo'])
        self.price_range.update(self.active_part['PriceRanges'])
        self.parameters.update(self.active_part['Parameters'])
        pass

