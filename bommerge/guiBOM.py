from gui import componentListWidget as componentList
from gui import mergeDialog as mergeDialog
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
    

def loadBOM(filename):
    bom = loadFile(filename)
    capacitors = {}
    capacitors['components'] = bom['Capacitors']
    capacitors['columns'] = capacitors['components'][0].keys()

    resistors = {}
    resistors['components'] = bom['Resistors']
    resistors['columns'] = resistors['components'][0].keys()

    inductors={}
    inductors['components'] = bom['Inductors']
    if inductors['components']:
        inductors['columns'] = inductors['components'][0].keys()

    integratedCircuits = {}
    integratedCircuits['components'] = bom['IntegratedCircuits']
    integratedCircuits['columns'] = integratedCircuits['components'][0].keys()

    connectors = {}
    connectors['components'] = bom['Connectors']
    if connectors['components']:
        connectors['columns'] = connectors['components'][0].keys()

    others = {}
    others['components'] = bom['Others']
    if others['components']:
        keys = set()
        for component in others['components']:
            for key in component.keys():
                keys.add(key)
        others['columns'] = list(keys)
    return {'Capacitors' : capacitors, 'Resistors' : resistors, 'Inductors' : inductors, 'IntegratedCircuits' : integratedCircuits, 'Connectors' : connectors,'Others' : others}
#colors = ['red', 'green', 'yellow', 'orange', 'blue', 'navy']


def createComponentWidget(root, columns, values):
    widget = componentList.ScrolledComponentsList(master=root, selectmode=tk.EXTENDED)  
    widget.addColumns(columns)
    for i, component in enumerate(values):
        if 'status' in component:
            widget.addItem(str(i), component, component['status'])
        else:
            widget.addItem(str(i), component)
    return widget


def refreshComponentWidget(widget, components):
    widget.removeAllItems()
    for i, component in enumerate(components):
        if 'status' in component:
            widget.addItem(str(i), component, component['status'])
        else:
            widget.addItem(str(i), component)


def createFrame(root, columns, components):
    frame = ttk.Frame(root)
    componentsWidget = createComponentWidget(frame, columns, components)
    componentsWidget.pack()
    button = tk.Button(frame, text='Merge', width=25, command= lambda : onMergeButtonPressed(root, componentsWidget, components))
    button.pack()
    return frame
    

def onMergeButtonPressed(parent, widget, components):
    componentsToMerge = []
    selectedIndices = widget.getSelectedIndices()
    for i in selectedIndices:
        componentsToMerge.append(components[i])

    merged = mergeDialog.MergeDialog(parent, widget.getDisplayedFieldsNames(), componentsToMerge)  
    if merged.result:
        selectedIndices.sort(reverse=True)
        for index in selectedIndices:
            del components[index]
        components.append(merged.result)
        components.sort()
        refreshComponentWidget(widget, components)


def validate_resistors(components):
    from partnameDecoder import resistors as resistorResolver

    def has_required_fields(part):
        required_fields = ['Resistance', 'Case']
        for field in required_fields:
           if not part[field] or part[field] == '':
               return False 
        return True   
        
    def validateParameters(part, resolved):
        fields_to_check = ['Resistance', 'Case', 'Tolerance']
        for field in fields_to_check:
            if field in resolved:
                if part[field] != resolved[field]:
                    print resolved
                    print str(field)
                    return False
        return True     
       
    for part in components:
        validation_status = None
        if not has_required_fields(part):
            validation_status = 'MissingParameters'
                
        if part['Manufacturer Part Number']:
            resolvedParameters = resistorResolver.resolve(part['Manufacturer Part Number'])
            if resolvedParameters:
                if validateParameters(part, resolvedParameters) == False:
                    validation_status = 'IncorrectParameters'
            else:
                validation_status = 'PartnumberDecoderMissing'
        if validation_status:
            print 'Resistor validation failded, status: ' + validation_status
            part['status'] = validation_status
                    
def validate_capacitors(components):
    from partnameDecoder import capacitors as capacitorResolver

    def has_required_fields(part):
        required_fields = ['Capacitance', 'Voltage', 'Case']
        for field in required_fields:
            if not part[field] or part[field] == '':
                return False 
        return True
        
    def validateParameters(part, resolved):
        fields_to_check = ['Capacitance', 'Voltage', 'Case', 'Tolerance']
        for field in fields_to_check:
            if field in resolved:
                if part[field] != resolved[field]:
                    return False
        return True
       
    for part in components:
        validation_status = None
        if not has_required_fields(part):
            validation_status = 'MissingParameters'
                
        if part['Manufacturer Part Number'] != '':
            resolvedParameters = capacitorResolver.resolve(part['Manufacturer Part Number'])
            if resolvedParameters:
                if validateParameters(part, resolvedParameters) == False:
                    validation_status = 'IncorrectParameters'
            else:
                validation_status = 'PartnumberDecoderMissing'

        if validation_status:
            print 'Capacitor validation failded, status: ' + validation_status
            part['status'] = validation_status


def createNotebook(root, components):
    notebook = ttk.Notebook(root)    
    
    validate_resistors(components['Resistors']['components'])
    validate_capacitors(components['Capacitors']['components'])

    if components['Resistors']['components']:
        frame = createFrame(root, ['Quantity', 'Resistance', 'Tolerance', 'Case', 'Manufacturer', 'Manufacturer Part Number'], components['Resistors']['components'])
        notebook.add(frame, text='Resistors')

    if components['Capacitors']['components']:
        frame = createFrame(root, ['Quantity', 'Capacitance', 'Voltage', 'Dielectric Type', 'Tolerance', 'Case', 'Manufacturer', 'Manufacturer Part Number'], components['Capacitors']['components'])
        notebook.add(frame, text='Capacitors')
       
    if components['Inductors']['components']:
        frame = createFrame(root, components['Inductors']['columns'], components['Inductors']['components'])
        notebook.add(frame, text='Inductors')

    if components['IntegratedCircuits']['components']:
        frame = createFrame(root, components['IntegratedCircuits']['columns'], components['IntegratedCircuits']['components'])
        notebook.add(frame, text='IC')

    if components['Connectors']['components']:
        frame = createFrame(root, components['Connectors']['columns'], components['Connectors']['components'])
        notebook.add(frame, text='Connectors')

    if components['Others']['components']:
        frame = createFrame(root,  components['Others']['columns'], components['Others']['components'])
        notebook.add(frame, text='Others')

    return notebook    
        
def onDoubleClick(event):
    item = resistorsWidget.getSelected()
    print("you clicked on", resistorsWidget.treeview.item(item,"text"))

def merge(filename):
    root = tk.Tk()
    root.title("BOM Merger")
    notebook = createNotebook(root, loadBOM(filename))
    notebook.pack()
    root.mainloop()

