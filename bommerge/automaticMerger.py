def convertCapacitanceToFarads(capacitance):
    import re    
    mul = {'F': 1,
           'mF': 0.001,
           'uF': 0.000001,
           'nF': 0.000000001,
           'pF': 0.000000000001,
           'fF': 0.000000000000001}

    if capacitance == None:
       return None
    separatedCapacitance = re.split('(\d+)', capacitance)
    if separatedCapacitance[-1] in mul:
        multiplier = mul[separatedCapacitance[-1]]
        value = float(capacitance[:-len(separatedCapacitance[-1])])
        value = value * multiplier
        return value

def convertResistanceToOhms(resistance):
    import re    
    mul = {'G': 1000000000,
           'M': 1000000,
           'k': 1000,
           'R': 1,
           'm': 0.001,
           'u': 0.000001}

    if resistance == None:
       return None
    separated = re.split('(\d+)', resistance)
    if separated[-1] in mul:
        multiplier = mul[separated[-1]]
        value = float(resistance[:-len(separated[-1])])
        value = value * multiplier
        return value

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
        self.components = sorted(self.components, key=self.valueForCompare)

    def toList(self):
        return self.components

    def _merge(self, part):
        i = self.getIndexOff(part)
        self.components[i]['Quantity'] = str(int(self.components[i]['Quantity']) + int(part['Quantity']))
        self.components[i]['Designator'] = self.components[i]['Designator'] + part['Designator']



class Resistors(ComponentContainer):
    @staticmethod
    def isSame(resA, resB):
        if convertResistanceToOhms(resA['Resistance']) != convertResistanceToOhms(resB['Resistance']):
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
        return convertResistanceToOhms(k['Resistance'])

class Capacitors(ComponentContainer):
    @staticmethod
    def isSame(capA, capB):        
        if convertCapacitanceToFarads(capA['Capacitance']) != convertCapacitanceToFarads(capB['Capacitance']):
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
        return convertCapacitanceToFarads(k['Capacitance'])

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

def loadFile(filename):
    print("Loading json file: " + filename)
    import json
    with open(filename) as inputFile:
        bom = json.load(inputFile)
    return bom

def saveFile(filename, content):
    import json
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(content, indent=4, sort_keys=True, separators=(',', ': ')))


def saveMerged(mergedBom, filename):
    fileContent = {'Capacitors': mergedBom['Capacitors'].toList(), 'Resistors': mergedBom['Resistors'].toList(), 'Inductors': mergedBom['Inductors'].toList(), 'IntegratedCircuits': mergedBom['IntegratedCircuits'].toList(), 'Connectors': mergedBom['Connectors'].toList(), 'Others': mergedBom['Others'].toList()}
    saveFile(filename, fileContent)

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
        bom = loadFile(bomFile['filename'])
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
        bom = loadFile(jsonFile)
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
    saveFile('merged.json', fileContent)
       


