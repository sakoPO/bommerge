from components import resistor
from components import capacitor
from utils import files

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
            return result if result != None else 0
            
        self.components = sorted(self.components, key=key)

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
        if partA['Inductance'] != partB['Inductance']:
            return False
        if partA['Case'] != partB['Case']:
            return False
        if partA['Manufacturer'] != partB['Manufacturer']:
            return False
        if partA['Manufacturer Part Number'] != partB['Manufacturer Part Number']:
            return False
        return True
    @staticmethod
    def valueForCompare(k):
        return k['Inductance']

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
        if partA['Comment'] != partB['Comment']:
            return False
        return True
    @staticmethod
    def valueForCompare(k):
        return k['Comment']


def convertCsvToJson(csvFile):    
    csvToJson.convert(csvFile, 'tmp')


def saveMerged(mergedBom, filename):
    fileContent = {'Capacitors': mergedBom['Capacitors'].toList(), 'Resistors': mergedBom['Resistors'].toList(), 'Inductors': mergedBom['Inductors'].toList(), 'IntegratedCircuits': mergedBom['IntegratedCircuits'].toList(), 'Connectors': mergedBom['Connectors'].toList(), 'Others': mergedBom['Others'].toList()}
    files.save_json_file(filename, fileContent)

def bomMultiply(bom, mul):
    for key in ['Capacitors', 'Resistors', 'Inductors', 'IntegratedCircuits', 'Connectors', 'Others']:
        for component in bom[key]:
            component['Quantity'] = int(component['Quantity']) * mul
    return bom    

def sortMergedComponents(merged):
    for key in ['Capacitors', 'Resistors', 'Inductors', 'IntegratedCircuits', 'Connectors', 'Others']:
        merged[key].sort()
    return merged        
    
def merge(jsonFileList, outputFilename):
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
    saveMerged(merged, outputFilename)
    
def main():
    for csvFile in fileList:
        convertCsvToJson(csvFile)

    capacitors = Capacitors()
    resistors = Resistors()
    inductors = Inductors()
    integratedCircuits = IntegratedCircuits()
    connectors = Connectors()
    others = Others()
    
    for jsonFile in jsonFileList:
        bom = files.load_json_file(jsonFile)
        for cap in bom['Capacitors']:
            capacitors.addUnique(cap, bom['filename'])
        for res in bom['Resistors']:
            resistors.addUnique(res, bom['filename'])
        for inductor in bom['Inductors']:
            inductors.addUnique(inductor, bom['filename'])
        for ic in bom['IntegratedCircuits']:
            integratedCircuits.addUnique(ic, bom['filename'])
        for connector in bom['Connectors']:
            connectors.addUnique(connector, bom['filename'])
        for component in bom['Others']:
            others.addUnique(component, bom['filename'])

    capacitors.sort()
    resistors.sort()
    inductors.sort()
    integratedCircuits.sort()
    connectors.sort()
    others.sort()

    fileContent = {'Capacitors': capacitors.toList(), 'Resistors': resistors.toList(), 'Inductors': inductors.toList(), 'IntegratedCircuits': integratedCircuits.toList(), 'Connectors': connectors.toList(), 'Others': others.toList()}
    files.save_json_file('merged.json', fileContent)
       


