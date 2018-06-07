import componentListWidget as componentList
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    
def loadFile(filename):
    import json
    with open(filename) as inputFile:
        bom = json.load(inputFile)
    return bom


class ComponentGroup(ttk.Frame):
    def __init__(self, parent, name, columns, components, validator_function = None):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = name
        self.components = components
        self.validate = validator_function
        self.create_gui(columns)
        self.refresh_widget()

#        if self.name == 'Capacitors':
#            self.value_key = 'Capacitance'
            #from partnameDecoder import capacitors as capacitorResolver
#            self.resolver = None#capacitorResolver
#        elif self.name == 'Resistors':
#            self.value_key = 'Resistance'
#            from partnameDecoder import resistors as resistorResolver
#            self.resolver = resistorResolver
#        else:
        self.value_key = 'Comment'
        self.resolver = None


    def create_gui(self, columns):
        def on_selection_change():
            if len(self.widget.getSelectedIndices()) > 1:
                self.button.config(state=tk.NORMAL)
            else:
                self.button.config(state=tk.DISABLED)

        self.widget = componentList.ScrolledComponentsList(master=self,
                                                           on_selction_change=on_selection_change,
                                                           on_item_double_click=self.on_item_double_click,
                                                           selectmode=tk.EXTENDED)
        self.widget.addColumns(columns)
        self.widget.pack(expand=True, fill=tk.BOTH)
        self.button = tk.Button(self, text='Merge', width=25, command=self.on_merge_button_pressed)
        self.button.config(state=tk.DISABLED)
        self.button.pack()


    def sort(self):
        if self.name == 'Capacitors':
            self.components.sort(key=lambda x: capacitor.convertCapacitanceToFarads(x['Capacitance']))
        elif self.name == 'Resistors':
            self.components.sort(key=lambda x: resistor.convertResistanceToOhms(x['Resistance']))
        else:
            self.components.sort()


    def refresh_widget(self):
        self.widget.removeAllItems()
        for i, component in enumerate(self.components):
            if self.validate:
                component['validation_status'] = self.validate(component)
            if 'validation_status' in component:
                self.widget.addItem(str(i), component, component['validation_status'])
            else:
                self.widget.addItem(str(i), component)
    

    def remove_components_by_indices(self, indices_list):
        indices_list.sort(reverse=True)
        for index in indices_list:
            tmp = self.components.pop(index)
            print("Removing component " + str(tmp[self.value_key]) + ', With index: ' + str(index))
        

    def on_merge_button_pressed(self):
        components_to_merge = []
        selected_indices = self.widget.getSelectedIndices()
        for i in selected_indices:
            components_to_merge.append(self.components[i])

        merged = mergeDialog.MergeDialog(self.parent, self.widget.getDisplayedFieldsNames(), components_to_merge)
        if merged.result:
            self.remove_components_by_indices(selected_indices)
            merged_component = dict(merged.result)
            self.components.append(merged_component)
            self.sort()
            self.refresh_widget()


    def on_item_double_click(self, event):
        item = self.widget.getSelectedIndices()
        print("you clicked on: ", item)
        component = self.components[item[0]]
        if 'Manufacturer Part Number' in component:
            resolved_parameters = self.resolver.resolve(component['Manufacturer Part Number'])
        partDetailDialog.PartDetailDialog(self.parent, component, resolved_parameters)


class SuppliersDetailsWidget(ttk.Frame):    
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.create_brief_view()
        self.create_order_quantity()
        self.create_distributor_selector()
        self.create_detail_view()
        self.create_detail_view()
        self.create_detail_view()
        self.create_detail_view()
        self.create_detail_view()


    def create_brief_view(self):
        pass

    def create_order_quantity(self):
        from widgets.order_quantity import order_quantity
        self.order_quantity = order_quantity(self)
        self.order_quantity.pack(anchor=tk.W, padx=10, pady=10)

    def create_distributor_selector(self):
        from widgets.distributor_selector import distributor_selector
        self.distributor_selector = distributor_selector(self)
        self.distributor_selector.pack(expand=True, fill=tk.X)

    def create_price_range(self, parent, ranges):
        from widgets.price_range import price_range
        return price_range(parent, ranges)


    def create_order_info(self, parent, order_info):
        frame = tk.LabelFrame(parent, text="Order information")
        min_order_label = tk.Label(frame, text='Minimal Order:')
        mul_order_label =  tk.Label(frame, text='Multiplicity:')
        stock_lavel = tk.Label(frame, text='Stock level:')
        min_order_label.grid(row=0, column=0)       
        mul_order_label.grid(row=1, column=0)
        stock_lavel.grid(row=2, column=0)
        min_order_value = tk.Label(frame, text=str(order_info['MinAmount']))
        mul_order_value =  tk.Label(frame, text=str(order_info['Mul']))
        stock_lavel_value = tk.Label(frame, text=str(order_info['Stock']))
        min_order_value.grid(row=0, column=1)       
        mul_order_value.grid(row=1, column=1)
        stock_lavel_value.grid(row=2, column=1)
        return frame

    def create_urls(self, parent):
        frame = ttk.Frame(parent)
        shop_url = tk.Label(frame, text=r"Component page", fg="blue", cursor="hand2")        
        shop_url.bind("<Button-1>", self.callback)
        datasheat_url = tk.Label(frame, text=r"Datasheat", fg="blue", cursor="hand2")        
        datasheat_url.bind("<Button-1>", self.callback)
        shop_url.pack(side=tk.LEFT, padx=10)
        datasheat_url.pack(side=tk.LEFT, padx=10)
        return frame

    def callback(self, event):
        import webbrowser
        webbrowser.open_new(event.widget.cget("text"))

    def crate_parameters(self, parent, parameters):
        frame = tk.LabelFrame(parent, text="Parameters")
        for i, parameter in enumerate(parameters):
            name_label = tk.Label(frame, text=str(parameter) + ': ' + str(parameters[parameter]))
            name_label.grid(row=i, sticky=tk.W, padx=10)       
        return frame

  

    def create_detail_view(self):
        def create_price_order_urls(parent):
            frame = ttk.Frame(parent)
            price_order_frame = ttk.Frame(frame)
            price_range = self.create_price_range(price_order_frame, [{'Amount':20, 'Price': 0.1620},{'Amount':100, 'Price': 0.1020}]) 
            price_range.pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)  
            order_info = self.create_order_info(price_order_frame, {'MinAmount': 10, 'Mul': 10, 'Stock': 123456})
            order_info.pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)
            price_order_frame.pack()
            urls = self.create_urls(frame)
            urls.pack(anchor=tk.W)
            return frame
  
        def on_item_double_click():
            pass
        def on_selection_change():
            pass
        
        frame = tk.LabelFrame(self, text="TME")
        components = componentList.ScrolledComponentsList(master=frame,
                                                           on_selction_change=on_selection_change,
                                                           on_item_double_click=on_item_double_click,
                                                           selectmode=tk.EXTENDED, height=4, show = 'headings')
        components.addColumns(['Manufacturer Part Number', 'Parameters', 'Price'])
        components.pack()
        another_frame = ttk.Frame(frame)
        parameters = self.crate_parameters(another_frame, {'Capacitance':'100nF', 'Voltage': '16V'})
        price_order = create_price_order_urls(another_frame)
        parameters.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        price_order.pack(side=tk.LEFT)
        another_frame.pack(expand=True, fill=tk.BOTH)
        frame.pack(expand=True, fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)


class OrderWidget(ttk.Notebook):
    def __init__(self, parent, filename):
        ttk.Notebook.__init__(self, parent)
        self.components = loadFile(filename)
        self.procees_components()
        self.create_bookmarks()
        self.pack(expand=True, fill=tk.BOTH)


    def _remove_keys_if_exist(self, keys, keys_to_remove):
        for key in keys_to_remove:
            if key in keys:
                keys.remove(key)
        return keys


    def procees_components(self):
        def combine(component, keys):
#            print("Combining parameters for: " + str(component))
            result = ''
            for key in reversed(keys):
                result = str(component[key]) + '; ' + result
            return result
                
        columns_to_combine = {'Resistors': ['Resistance', 'Tolerance', 'Case'], 'Capacitors': ['Capacitance', 'Voltage', 'Dielectric Type', 'Tolerance', 'Case']}
        for component_group in self.components.keys():
            for component in self.components[component_group]:
                component['Price'] = 0
                component['Order Quantity'] = ''
                component['Supplier'] = ''
                if component_group in columns_to_combine:
                    component['Parameters'] = combine(component, columns_to_combine[component_group])


    def create_component_columns(self, component):
        def sort(x):
            keys = {'Quantity': 1, 'Comment': 2, 'Description': 3, 'Manufacturer Part Number': 4, 'Manufacturer': 5}
            if x in keys:
                return keys[x]
            return 99

        keys = component
        keys = self._remove_keys_if_exist(keys, ['Designator'])
        keys.sort(key=sort)
        return keys


    def create_bookmarks(self):
        def sort(x):
            key = {'Capacitors': 1, 'Resistors': 2, 'Others': 100}
            if x in key:
                return key[x]
            return 99

        components_group = self.components.keys()
        components_group.sort(key=sort)
        for group in components_group:
            if self.components[group]:
                if group == 'Resistors':
                    columns_to_display = ['Quantity', 'Parameters', 'Manufacturer Part Number', 'Order Quantity', 'Price', 'Supplier']
                    validator = None#validate_resistor
                elif group == 'Capacitors':
                    columns_to_display = ['Quantity', 'Parameters', 'Manufacturer Part Number', 'Order Quantity', 'Price', 'Supplier']
                    validator = None#validate_capacitor
                elif group == 'Others':
                    keys = set()
                    for component in self.components[group]:
                        for key in component.keys():
                            keys.add(key)
                    columns_to_display = self.create_component_columns(list(keys))
                    validator = None
                else:
                    columns_to_display = self.create_component_columns(self.components[group][0].keys())                                     
                    validator = None                    
                columns_to_display = self._remove_keys_if_exist(columns_to_display, ['Manufacturer', 'Description', 'Footprint', 'LibRef'])   

                bookmark_layout = ttk.Frame(self)
                component_frame = ComponentGroup(bookmark_layout, group, columns_to_display, self.components[group], validator)
                component_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
                supplier_frame = SuppliersDetailsWidget(bookmark_layout) 
                supplier_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
                bookmark_layout.pack()
                self.add(bookmark_layout, text=group)    
    
def main(filename):
    root = tk.Tk()
    root.title("BOM Merger")
    manualMerger = OrderWidget(root, filename)
    root.mainloop()
    
if __name__ == "__main__":
    main("../../tests/tmp/automerged.json")    
