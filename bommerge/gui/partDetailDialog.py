try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

class PartDetailDialog(tk.Toplevel):
    def __init__(self, parent, component, decoded):
        tk.Toplevel.__init__(self, parent)
        self.title("Component details")
        self.parent = parent
        self.result = None

        columns = self.sort_columns(list(component.keys()))
        if 'Designator' in columns:
            columns.remove('Designator')
        if 'validation_status' in columns:
            columns.remove('validation_status')
        
        if decoded == None:
            decoded = []

        self.components_table = self._createComponentsTable(columns, [component, decoded])
        self.components_table.pack(expand=True, fill=tk.BOTH)
        self.partname_frame = self.create_frame_with_parameters_decoded_from_partname(decoded)
        self.partname_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10, ipadx=10, ipady=10)

        self.origin_frame = self.create_origin_frame(component)
        self.origin_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10, ipadx=10, ipady=10)
        self.pack_propagate()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.wait_window(self)


    def sort_columns(self, columns):
        def sort(x):
            keys = {'Quantity': 1, 'Designator': 99}
            if x in keys:
                return keys[x]
            return 98

        columns.sort(key=sort)
        return columns


    def _createComponentsTable(self, columns, components):
        parent = ttk.Frame(self)
        bom_parameters_label = tk.Label(parent, text='BOM Parameters')
        bom_parameters_label.grid(row=1, column=0)
        decoded_parameters_label = tk.Label(parent, text='Partname Parameters')
        decoded_parameters_label.grid(row=2, column=0)
        for c, column in enumerate(columns):
            c = c + 1
            l = tk.Label(parent, text=column)
            l.grid(row=0, column=c, padx=10)
            for r, component in enumerate(components):
                e = tk.Entry(parent, disabledbackground='white', disabledforeground='black')
                if column in component and component[column]:
                    e.insert(1, component[column])
                e.grid(row=r+1, column=c)
                e.config(state=tk.DISABLED)
        parent.grid_propagate()
        return parent


    def create_frame_with_parameters_decoded_from_partname(self, decoded_parameters):
        frame = tk.LabelFrame(self, text="Parameters decoded from partname")
        if decoded_parameters == []:
            missing_part_number = tk.Label(frame, text="Unable do decode parameters. Part number missing or unsupported part number.")
            missing_part_number.pack()
        else:
            for i, parameter in enumerate(decoded_parameters):
                name_label = tk.Label(frame, text=str(parameter) + ': ' + str(decoded_parameters[parameter]))
                name_label.grid(row=i, sticky=tk.W, padx=10)
        return frame


    def create_origin_frame(self, component):
        frame = tk.LabelFrame(self, text="Component orignin")
        for i, designators in enumerate(component['Designator'].splitlines()):
            name_label = tk.Label(frame, text=designators)
            name_label.grid(row=i, sticky=tk.W)
        return frame    


    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

