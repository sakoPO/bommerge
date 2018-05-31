from gui import componentListWidget as componentList
from gui import mergeDialog as mergeDialog
from gui import partDetailDialog as partDetailDialog
from components import capacitor
from components import resistor
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


def validate(part, partname_resolver, required_fields, fields_to_check):
    def has_required_fields(part):
        for field in required_fields:
           if not part[field] or part[field] == '':
               return False
        return True

    def validateParameters(part, resolved):
        for field in fields_to_check:
            if field in resolved:
                if part[field] != resolved[field]:
                    print resolved
                    print str(field)
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
        print 'Part validation failded, status: ' + validation_status
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
            print ("Removing component " + str(tmp[self.value_key]) + ', With index: ' + str(index))
        

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


class ManualMerger(ttk.Notebook):
    def __init__(self, parent, filename):
        ttk.Notebook.__init__(self, parent)
        self.components = loadFile(filename)
        self.create_bookmarks()
        self.pack(expand=True, fill=tk.BOTH)

    def create_component_columns(self, component):
        def remove_key(key):
            if key in keys:
                keys.remove(key)
            return keys

        def sort(x):
            keys = {'Quantity': 1, 'Comment': 2, 'Description': 3, 'Manufacturer Part Number': 4, 'Manufacturer': 5}
            if x in keys:
                return keys[x]
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

        components_group = self.components.keys()
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
                    columns = self.create_component_columns(self.components[group][0].keys())
                    validator = None

                frame = ComponentGroup(self, group, columns, self.components[group], validator)
                self.add(frame, text=group)


def merge(filename):
    root = tk.Tk()
    root.title("BOM Merger")
    manualMerger = ManualMerger(root, filename)
    root.mainloop()

