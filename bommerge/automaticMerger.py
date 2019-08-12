from components import resistor
from components import capacitor
from utils import files
from functools import cmp_to_key

class ComponentContainer:
    def __init__(self):
        self.components = []

    @staticmethod
    def isSame(componentA, componentB):
        raise RuntimeError('Unimplemented method')

    @staticmethod
    def valueForCompare(k):
        raise RuntimeError('Unimplemented method')

    @staticmethod
    def transform(part, filename):
        newPart = part
        newPart['Designator'] = filename + ': ' + part['Designator'] + '\n'
        return part

    def contain(self, part):
        for component in self.components:
            if self.isSame(component, part):
                return True  
        return False

    def addUnique(self, part, filename):
        newPart = self.transform(part, filename)
        if not self.components:
            self.components.append(newPart)
        else:
            if not self.contain(newPart):
                self.components.append(newPart)
            else:
                self._merge(newPart)

    def getIndexOff(self, part):
        for i, component in enumerate(self.components):
            if self.isSame(component, part):
                return i
        return None

    def sort(self):
        def key(value):
            result = self.valueForCompare(value)
            if result == 'DNF':
                return -1
            print(result)
            return result if result is not None else 0

        def cmp_items(a, b):
            a_value = self.valueForCompare(a)
            b_value = self.valueForCompare(b)
            if a_value is None:
                a_value = 0
            elif a_value == "DNF":
                a_value = -1
            if b_value is None:
                b_value = 0
            elif b_value == "DNF":
                b_value = -1

            try:
                if a_value > b_value:
                    return 1
                elif a_value == b_value:
                    return 0
                else:
                    return -1
            except TypeError:
                if isinstance(a_value, str):
                    return 1
                else:
                    return -1
            
        self.components = sorted(self.components, key=cmp_to_key(cmp_items))

    def toList(self):
        return self.components

    def _merge(self, part):
        i = self.getIndexOff(part)
        self.components[i]['Quantity'] = str(int(self.components[i]['Quantity']) + int(part['Quantity']))
        self.components[i]['Designator'] = self.components[i]['Designator'] + part['Designator']


class Resistors(ComponentContainer):
    @staticmethod
    def isSame(resA, resB):
        if resistor.convert_resistance_to_ohms(resA['Resistance']) != resistor.convert_resistance_to_ohms(resB['Resistance']):
            return False
        if resA['Case'] != resB['Case']:
            return False
        if resA['Manufacturer'] != resB['Manufacturer']:
            return False
        if resA['Manufacturer Part Number'] != resB['Manufacturer Part Number']:
            return False
        return True
    @staticmethod
    def valueForCompare(k):
        return resistor.convert_resistance_to_ohms(k['Resistance'])


class Capacitors(ComponentContainer):
    @staticmethod
    def isSame(capA, capB):        
        if capacitor.convert_capacitance_co_farads(capA['Capacitance']) != capacitor.convert_capacitance_co_farads(capB['Capacitance']):
            return False
        if capA['Case'] != capB['Case']:
            return False
        if capA['Dielectric Type'] != capB['Dielectric Type']:
            return False
        if capA['Voltage'] != capB['Voltage']:
            return False
        if capA['Manufacturer'] != capB['Manufacturer']:
            return False
        if capA['Manufacturer Part Number'] != capB['Manufacturer Part Number']:
            return False
        return True
    @staticmethod
    def valueForCompare(k):
        return capacitor.convert_capacitance_co_farads(k['Capacitance'])


class Inductors(ComponentContainer):
    @staticmethod
    def isSame(partA, partB):
        if 'Inductance' in partA and 'Iinductance' in partB:
            if partA['Inductance'] != partB['Inductance']:
                return False
        if 'Case' in partA and 'Case' in partB:
            if partA['Case'] != partB['Case']:
                return False
        if 'Manufacturer' in partA and 'Manufacturer' in partB:
            if partA['Manufacturer'] != partB['Manufacturer']:
                return False
        if 'Manufacturer Part Number' in partA and 'Manufacturer Part Number' in partB:
            if partA['Manufacturer Part Number'] != partB['Manufacturer Part Number']:
                return False
            return True


    @staticmethod
    def valueForCompare(k):
        if 'Inductance' in k:
            return k['Inductance']
        return None


class IntegratedCircuits(ComponentContainer):
    @staticmethod
    def isSame(partA, partB):
        if partA['Comment'] != partB['Comment']:
            return False
        if partA['Manufacturer'] != partB['Manufacturer']:
            return False
        if partA['Manufacturer Part Number'] != partB['Manufacturer Part Number']:
            return False
        return True
    @staticmethod
    def valueForCompare(k):
        return k['Manufacturer Part Number']


class Connectors(ComponentContainer):
    @staticmethod
    def isSame(partA, partB):
        if partA['Comment'] != partB['Comment']:
            return False
        if partA['Manufacturer'] != partB['Manufacturer']:
            return False
        if partA['Manufacturer Part Number'] != partB['Manufacturer Part Number']:
            return False
        return True
    @staticmethod
    def valueForCompare(k):
        return k['Manufacturer Part Number']


class Others(ComponentContainer):
    @staticmethod
    def isSame(partA, partB):
        if 'Comment' in partA and 'Comment' in partB:
            if partA['Comment'] == partB['Comment']:
                return True
        return False
    @staticmethod
    def valueForCompare(k):
        if 'Comment' not in k:
            return None
        return k['Comment']


def bomMultiply(bom, mul):
    for key in ['Capacitors', 'Resistors', 'Inductors', 'IntegratedCircuits', 'Connectors', 'Others']:
        for component in bom[key]:
            component['Quantity'] = int(component['Quantity']) * mul
    return bom    


def sortMergedComponents(merged):
    for key in ['Capacitors', 'Resistors', 'Inductors', 'IntegratedCircuits', 'Connectors', 'Others']:
        merged[key].sort()
    return merged        


def convert_to_dictionary(mergedBom):
    return {'Capacitors': mergedBom['Capacitors'].toList(), 'Resistors': mergedBom['Resistors'].toList(), 'Inductors': mergedBom['Inductors'].toList(), 'IntegratedCircuits': mergedBom['IntegratedCircuits'].toList(), 'Connectors': mergedBom['Connectors'].toList(), 'Others': mergedBom['Others'].toList()}


def merge(jsonFileList):
    merged = {}
    merged['Capacitors'] = Capacitors()
    merged['Resistors'] = Resistors()
    merged['Inductors'] = Inductors()
    merged['IntegratedCircuits'] = IntegratedCircuits()
    merged['Connectors'] = Connectors()
    merged['Others'] = Others()
    
    for bomFile in jsonFileList:
        bom = files.load_json_file(bomFile['filename'])
        bom = bomMultiply(bom, bomFile['Quantity'])
        for key in ['Capacitors', 'Resistors', 'Inductors', 'IntegratedCircuits', 'Connectors', 'Others']:
            for component in bom[key]:
                merged[key].addUnique(component, bom['filename'])

    merged = sortMergedComponents(merged)
    return convert_to_dictionary(merged)

