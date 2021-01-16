from validators import validator as Validator
from partnameDecoder import capacitors as capacitorResolver
from partnameDecoder import resistors as resistorResolver
from components import capacitor
from components import resistor


class ComponentsGroup:
    def __init__(self, name, components):
        self.name = name
        self.components = components
        self.validation_status = []
        self.partname_resolver = None
        self.visible_parameters = []
        self.__init_visible_fields_and_validator()
        self.validate()

    def get_component(self, index):
        return self.components[index]

    def get_component_count(self):
        return len(self.components)

    def remove_components_by_index(self, indices):
        indices.sort(reverse=True)
        for item in indices:
            del self.components[item]

    def resolve_component_parameters(self, index):
        if self.partname_resolver is not None:
            return self.partname_resolver.resolve(self.components[index]['Manufacturer Part Number'])

    def append(self, component):
        self.components.append(component)
        self.sort()

    def validate(self):
        for i, component in enumerate(self.components):
            if self.validator is not None:
                self.validation_status.insert(i, self.validator(component))
            else:
                self.validation_status.insert(i, None)

    def sort(self):
        def resistors_key(x):
            if x['Resistance'] == 'DNF':
                return -1
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

    def __init_visible_fields_and_validator(self):
        if self.name == 'Resistors':
            self.visible_parameters = ['Quantity', 'Resistance', 'Tolerance', 'Case', 'Manufacturer', 'Manufacturer Part Number']
            self.validator = Validator.validate_resistor
            self.partname_resolver = resistorResolver
        elif self.name == 'Capacitors':
            self.visible_parameters = ['Quantity', 'Capacitance', 'Voltage', 'Dielectric Type', 'Tolerance', 'Case', 'Manufacturer',
                       'Manufacturer Part Number']
            self.validator = Validator.validate_capacitor
            self.partname_resolver = capacitorResolver
        elif self.name == 'Others':
            keys = set()
            for component in self.components:
                for key in component.keys():
                    keys.add(key)
            self.visible_parameters = self.create_component_columns(list(keys))
            self.validator = None
        elif len(self.components) > 0:
            self.visible_parameters = self.create_component_columns(list(self.components[0].keys()))
            self.validator = None
        else:
            self.visible_parameters = ['Quantity', 'Manufacturer', 'Manufacturer Part Number']
            self.validator = None

    @staticmethod
    def create_component_columns(component):
        def remove_key(key):
            if key in keys:
                keys.remove(key)
            return keys

        def sort(x):
            keys_dict = {'Quantity': 1, 'Comment': 2, 'Description': 3, 'Manufacturer Part Number': 4,
                         'Manufacturer': 5}
            if x in keys_dict:
                return keys_dict[x]
            return 99

        keys = component
        keys = remove_key('Designator')
        keys.sort(key=sort)
        return keys