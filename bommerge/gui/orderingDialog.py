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
    def __init__(self, parent, name, columns, components, validator_function = None, on_selection=None):
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
        self.on_selection_change = on_selection


    def create_gui(self, columns):
        def on_selection_change():
            if self.on_selection_change:
                self.on_selection_change(self.widget.getSelectedIndices())

        self.widget = componentList.ScrolledComponentsList(master=self,
                                                           on_selction_change=on_selection_change,
                                                           on_item_double_click=self.on_item_double_click)
        self.widget.addColumns(columns)
        self.widget.pack(expand=True, fill=tk.BOTH)
#        self.button = tk.Button(self, text='Merge', width=25, command=self.on_merge_button_pressed)
#        self.button.config(state=tk.DISABLED)
#        self.button.pack()


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


def get_price(quantity, price_ranges):
    for price in reversed(price_ranges):
        if quantity >= price['Amount']:
            return price['Price']
    print price_ranges
    raise RuntimeError("Unable to match price range. Required quantity: " + str(quantity))

def add_component_price(component):    
    required_quantity = int(component['Quantity'])
    for distributor in component['Distributors']:
        for component in distributor['Components']:
            order_info = component['OrderInfo']            
            if required_quantity <= order_info['MinAmount']:
                order_quantity = order_info['MinAmount']
            else:
                mul = (required_quantity - int(order_info['MinAmount'])) / int(order_info['Multiples'])
                order_quantity = int(order_info['MinAmount']) + int(order_info['Multiples']) * mul
                if order_quantity < required_quantity:
                    order_quantity = order_quantity + order_info['Multiples']
            component['Price'] = get_price(order_quantity, component['PriceRanges']) * order_quantity
            component['OrderQuantity'] = order_quantity
            


class SuppliersDetailsWidget(ttk.Frame):    
    def __init__(self, parent, components, on_order_change):
        ttk.Frame.__init__(self, parent)
        self.components = components
        self.on_order_change = on_order_change        
        self.supplier = []
        self.create_brief_view()
        self.create_order_quantity()
        self.create_distributor_selector()
        for component in components:            
            self.create_detail_view(component)


    def create_brief_view(self):
        pass


    def create_order_quantity(self):
        from widgets.order_quantity import order_quantity
        self.order_quantity = order_quantity(self, self._on_quantity_change)
        self.order_quantity.pack(anchor=tk.N + tk.W, padx=10, pady=10)


    def create_distributor_selector(self):
        from widgets.distributor_selector import distributor_selector
        self.distributor_selector = distributor_selector(self, self._on_distributor_change)
        distributors = ['None']
        for distributor in self.components:
            distributors.append(distributor['Name'])
        self.distributor_selector.activate(distributors)
        self.distributor_selector.pack(anchor=tk.N + tk.W)
  

    def create_detail_view(self, distributor):
        from widgets.supplier_info import supplier_info as supplier_info
        supplier = supplier_info(self, distributor['Name'], distributor['Components'], self._on_change)
        supplier.pack(anchor=tk.N, expand=True, fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
        self.supplier.append(supplier)


    def validate_quantity(self, component):
        quantity = self.order_quantity.get()
        order_info = component['OrderInfo']
        if not quantity or quantity < order_info['MinAmount']:
            return False
        if (quantity - order_info['MinAmount']) % order_info['Multiples'] != 0:
            return False
        return True


    def calculate_price(self, component):
        order_quantity = self.order_quantity.get()
        return get_price(order_quantity, component['PriceRanges']) * order_quantity
        

    def get_component_by_distributor(self, distributor):
        print("Loking for component from: " + distributor)
        for i, component in enumerate(self.components):
            if component['Name'] == distributor:
                return component['Components'][self.supplier[i].get_active_part_index()]


    def _update_order_info(self, distributor):
        component = self.get_component_by_distributor(distributor)
        if distributor not in ['None', 'PartKeeper']:
            if self.validate_quantity(component) == False:
                self.order_quantity.make_invalid()
                return
           
        self.order_quantity.make_valid()
        price = 0 if distributor == 'None' else self.calculate_price(component)
        quantity = 0 if distributor == 'None' else self.order_quantity.get()
        if self.on_order_change:
            self.on_order_change(distributor, quantity, price)
            
 
    def _on_distributor_change(self, distributor):
        self._update_order_info(distributor)


    def _on_quantity_change(self, quantity):
        self._update_order_info(self.distributor_selector.get())


    def _on_change(self):
        self._update_order_info(self.distributor_selector.get())


        

class Bookmark(ttk.Frame):
    def __init__(self, parent, group, columns_to_display, components, validator):
        ttk.Frame.__init__(self, parent)
        self.components = components
        self.active_component_index = 0
        self.component_frame = ComponentGroup(self, group, columns_to_display, components, validator, self.on_selection)
        self.component_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.supplier_frame = [] 
        for component in components:
            self.supplier_frame.append(SuppliersDetailsWidget(self, component['Distributors'], self.on_component_order_change))
        self.supplier_frame[0].pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


    def on_selection(self, index):
        print index
        self.active_component_index = index[0]
        for i, supplier_frame in enumerate(self.supplier_frame):
            if i == index[0]:
                supplier_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            else:
                supplier_frame.pack_forget()


    def on_component_order_change(self, distributor, quantity, price):
        self.components[self.active_component_index]['Supplier'] = distributor
        self.components[self.active_component_index]['Order Quantity'] = quantity
        self.components[self.active_component_index]['Price'] = price
        self.component_frame.refresh_widget()
        pass
        

class OrderWidget(ttk.Notebook):
    def __init__(self, parent, filename):
        ttk.Notebook.__init__(self, parent)
        self.components = loadFile(filename)
        for group in self.components.keys():
            for component in self.components[group]:
                add_component_price(component)
        self.supplier_frame = {}
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

    def on_selection(self, index):
        print index
        for i, supplier_frame in enumerate(self.supplier_frame["Capacitors"]):
            if i == index[0]:
                supplier_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            else:
                supplier_frame.pack_forget()
        


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

                bookmark_layout = Bookmark(self, group, columns_to_display, self.components[group], validator)
                bookmark_layout.pack()
                self.add(bookmark_layout, text=group)    

    
def main(filename):
    root = tk.Tk()
    root.title("BOM Merger")
    manualMerger = OrderWidget(root, filename)
    root.mainloop()
    
if __name__ == "__main__":
    main("orderingDialogTestData.json")    
