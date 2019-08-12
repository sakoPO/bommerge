from gui import componentListWidget as componentList
from gui import mergeDialog as mergeDialog
from gui import partDetailDialog as partDetailDialog
from components import capacitor
from components import resistor
from utils import files
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


def validate(part, partname_resolver, required_fields, fields_to_check):
    def has_required_fields(part):
        for field in required_fields:
           if not part[field] or part[field] == '':
               return False
        return True

    def validateParameters(part, resolved):
        for field in fields_to_check:
            if field in resolved:
                if field in ['Capacitance']:
                    if capacitor.convert_capacitance_co_farads(part[field]) != capacitor.convert_capacitance_co_farads(resolved[field]):
                        print(resolved)
                        print(str(field) + ' ' + str(part[field]) + ' ' + resolved[field])
                        return False
                elif field in ['Resistance']:
                    if resistor.convert_resistance_to_ohms(part[field]) != resistor.convert_resistance_to_ohms(resolved[field]):
                        print(resolved)
                        print(str(field) + ' ' + str(part[field]) + ' ' + resolved[field])
                        return False
                elif field in ['Voltage']:
                    if part[field].replace('VDC', 'V') != resolved[field].replace('VDC', 'V'):
                        print(resolved)
                        print(str(field) + ' ' + str(part[field]) + ' ' + resolved[field])
                        return False
                elif part[field] != resolved[field]:
                    print(resolved)
                    print(str(field))
                    return False
        return True

    validation_status = None
    if not has_required_fields(part):
        validation_status = 'MissingParameters'

    if part['Manufacturer Part Number']:
        resolvedParameters = partname_resolver.resolve(part['Manufacturer Part Number'])
        if resolvedParameters:
            if validateParameters(part, resolvedParameters) == False:
                validation_status = 'IncorrectParameters'
        else:
            validation_status = 'PartnumberDecoderMissing'
    if validation_status:
        print('Part validation failded, status: ' + validation_status)
    return validation_status


def validate_resistor(part):
    from partnameDecoder import resistors as resistorResolver
    required_fields = ['Resistance', 'Case']
    fields_to_check = ['Resistance', 'Case', 'Tolerance']
    return validate(part, resistorResolver, required_fields, fields_to_check)


def validate_capacitor(part):
    from partnameDecoder import capacitors as capacitorResolver
    required_fields = ['Capacitance', 'Voltage', 'Case']
    fields_to_check = ['Capacitance', 'Voltage', 'Case', 'Tolerance']
    return validate(part, capacitorResolver, required_fields, fields_to_check)


class ComponentGroup(ttk.Frame):
    def __init__(self, parent, name, columns, components, validator_function = None):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = name
        self.components = components
        self.validate = validator_function
        self.create_gui(columns)
        self.refresh_widget()

        if self.name == 'Capacitors':
            self.value_key = 'Capacitance'
            from partnameDecoder import capacitors as capacitorResolver
            self.resolver = capacitorResolver
        elif self.name == 'Resistors':
            self.value_key = 'Resistance'
            from partnameDecoder import resistors as resistorResolver
            self.resolver = resistorResolver
        else:
            self.value_key = 'Comment'
            self.resolver = None

    def create_gui(self, columns):
        def on_selection_change():
            if len(self.widget.getSelectedIndices()) > 1:
                self.button.config(state=tk.NORMAL)
            else:
                self.button.config(state=tk.DISABLED)

            if len(self.widget.getSelectedIndices()) >= 1:
                self.button_delete.config(state=tk.NORMAL)
            else:
                self.button_delete.config(state=tk.DISABLED)

        self.widget = componentList.ScrolledComponentsList(master=self,
                                                           on_selction_change=on_selection_change,
                                                           on_item_double_click=self.on_item_double_click,
                                                           selectmode=tk.EXTENDED)
        self.widget.addColumns(columns)
        self.widget.pack(expand=True, fill=tk.BOTH)
        self.button_frame = ttk.Frame(self)
        self.button = tk.Button(self.button_frame, text='Merge', command=self.on_merge_button_pressed)
        self.button.config(state=tk.DISABLED)
        self.button.pack(side=tk.LEFT)
        self.button_delete = tk.Button(self.button_frame, text='Delete', command=self.on_delete_button_pressed)
        self.button_delete.config(state=tk.DISABLED)
        self.button_delete.pack(side=tk.LEFT)
        self.order_button = tk.Button(self.button_frame, text='Start Ordering', command=self.parent.start_order)
        self.order_button.pack(side=tk.LEFT)
        self.cancel_button = tk.Button(self.button_frame, text='Cancel', command=self.parent.cancel)
        self.cancel_button.pack(side=tk.LEFT)
        self.button_frame.pack()

    def sort(self):
        def resistors_key(x):
            if x['Resistance'] == 'DNR':
                return -1;
            if x['Resistance'] is not None:
                return resistor.convert_resistance_to_ohms(x['Resistance'])
            return 0

        def capacitors_key(x):
            if x['Capacitance'] == 'DNF':
                return -1
            if x['Capacitance'] is not None:
                return capacitor.convert_capacitance_co_farads(x['Capacitance'])
            return 0

        if self.name == 'Capacitors':
            self.components.sort(key=capacitors_key)
        elif self.name == 'Resistors':
            self.components.sort(key=resistors_key)
        else:
            try:
                self.components.sort()
            except TypeError as e:
                print(e)
                pass

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
            try:
                print("Removing component " + str(tmp[self.value_key]) + ', With index: ' + str(index))
            except KeyError:
                print("Removing component, With index: " + str(index))

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

    def on_delete_button_pressed(self):
        selected_indices = self.widget.getSelectedIndices()
        self.remove_components_by_indices(selected_indices)
        self.refresh_widget()

    def on_item_double_click(self, event):
        item = self.widget.getSelectedIndices()
        print("you clicked on: ", item)
        component = self.components[item[0]]
        if 'Manufacturer Part Number' in component:
            if self.resolver:
                resolved_parameters = self.resolver.resolve(component['Manufacturer Part Number'])
            else:
                resolved_parameters = None
        partDetailDialog.PartDetailDialog(self.parent, component, resolved_parameters)


class ManualMerger(ttk.Notebook):
    def __init__(self, parent, components):        
        ttk.Notebook.__init__(self, parent)
        self.parent = parent
        self.components = components
        self.result = None
        self.create_bookmarks()
        self.pack(expand=True, fill=tk.BOTH)

    def cancel(self):
        self.parent.destroy()

    def start_order(self):
        self.result = True
        self.parent.destroy()

    def create_component_columns(self, component):
        def remove_key(key):
            if key in keys:
                keys.remove(key)
            return keys

        def sort(x):
            keys_dict = {'Quantity': 1, 'Comment': 2, 'Description': 3, 'Manufacturer Part Number': 4, 'Manufacturer': 5}
            if x in keys_dict:
                return keys_dict[x]
            return 99

        keys = component
        keys = remove_key('Designator')
        keys.sort(key=sort)
        return keys

    def create_bookmarks(self):
        def sort(x):
            key = {'Capacitors': 1, 'Resistors': 2, 'Others': 100}
            if x in key:
                return key[x]
            return 99

        components_group = list(self.components.keys())
        components_group.sort(key=sort)
        for group in components_group:
            if self.components[group]:
                if group == 'Resistors':
                    columns = ['Quantity', 'Resistance', 'Tolerance', 'Case', 'Manufacturer', 'Manufacturer Part Number']
                    validator = validate_resistor
                elif group == 'Capacitors':
                    columns = ['Quantity', 'Capacitance', 'Voltage', 'Dielectric Type', 'Tolerance', 'Case', 'Manufacturer', 'Manufacturer Part Number']
                    validator = validate_capacitor
                elif group == 'Others':
                    keys = set()
                    for component in self.components[group]:
                        for key in component.keys():
                            keys.add(key)
                    columns = self.create_component_columns(list(keys))
                    validator = None
                else:
                    columns = self.create_component_columns(list(self.components[group][0].keys()))
                    validator = None

                frame = ComponentGroup(self, group, columns, self.components[group], validator)
                self.add(frame, text=group)


def merge(filename):
    root = tk.Tk()
    root.title("BOM Merger")
    components = files.load_json_file(filename)
    manualMerger = ManualMerger(root, components)
    root.mainloop()
    if manualMerger.result:
        return manualMerger.components

