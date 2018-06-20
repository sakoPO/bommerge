import csv
import re
from components import resistor
from components import capacitor

def convertMetricSMDToImperialSMD(caseCode):
    return False

def removeNumberFromDesignator(designator):
    import re
    match = re.match(r'([A-Za-z]+)\d+', designator)
    if match:
        return match.group(1)
    return ''

def isCapacitor(component):
    if 'Capacitance' in component:
        if component['Capacitance'] != '':
            return True    
    if removeNumberFromDesignator(component['Designator']) == 'C':
        return True
    return False

def isResistor(component):
    if 'Resistance' in component:
        if component['Resistance'] != '':
            return True
    if removeNumberFromDesignator(component['Designator']) == 'R':
        return True
    return False

def isInductor(component):
    if 'Inductance' in component:
        if component['Inductance'] != '':
            return True
    if removeNumberFromDesignator(component['Designator']) == 'L':
        return True
    return False

def isTransistor(component):
    if removeNumberFromDesignator(component['Designator']) == 'Q':
        return True
    return False

def isIntegratedCircuit(component):
    designatorAlpha = removeNumberFromDesignator(component['Designator'])
    if designatorAlpha == 'U' or designatorAlpha == 'IC':
        return True
    return False

def isConnector(component):
    if removeNumberFromDesignator(component['Designator']) == 'J':
        return True
    return False

def isIgnorable(component):
    return False

def footprintDecoder(footprint):
    metricCase =   [ '0402', '0603', '1005', '1608', '2012', '2520', '3216', '3225', '4516', '4532', '5025', '6332']
    imperialCase = ['01005', '0201', '0402', '0603', '0805', '1008', '1206', '1210', '1806', '1812', '2010', '2512']
    

def getQuantity(component):
    for field in ['Quantity', 'quantity', 'Qty', 'qty']:
        if field in component:
            return component[field]
    raise RuntimeError("Unable to decode quantity form component" + str(component))

def getCase(component):
    imperialCase = ['01005', '0201', '0402', '0603', '0805', '1008', '1206', '1210', '1806', '1812', '2010', '2512']
    for field in ['Comment', 'Description']: 
        if field in component:
            for word in component[field].split():
                for case in imperialCase:
                    if case == word or (case + ';') == word or (case + ',') == word:
                        return case
    if 'RESC1608' in component['Footprint'] or 'CAPC1608' in component['Footprint']:
        return '0603'
    return None

def getTolerance(component):
    for field in ['Tolerance', 'tolerance']:
        if field in component:
            if component[field] != '':
                return component[field]
    for field in ['Comment', 'Description']:
        match = re.search('(\d+[%])', component[field]) 
        if match:
            return match.group(1)

def decodeCapacitor(component):
    def getCapacitance(component):
        import re
        for field in ['Capacitance', 'capacitance']:
            if field in component:
                if component[field] != '':
                    return component[field].replace(" ", "").replace(",", ".")
       
        for field in ['Comment', 'Description']:
            fieldContent = component[field]
            match = re.search(r'(\d+(F|m|u|n|p)\d+)', fieldContent) # try to match 4p7 4n7 4F1 etc.
            if match:
                return match.group(1).replace(" ", "").replace(",", ".")
            match = re.search(r'(\d+([.,]\d+)?[ ]?(F|mF|uF|nF|pF|m|u|n|p))', fieldContent) # try to match 4.7F 4,7F 4.7nF etc.
            if match:
                return match.group(1).replace(" ", "").replace(",", ".")


    def getVoltage(component):
        import re
        for field in ['Voltage', 'voltage']: 
            if field in component:
                if component[field] != '':
                    return component[field]

        for field in ['Comment', 'Description']: 
            if field in component:
               fieldContent = component[field]
               match = re.search(r'(\d+ ?(V|v))', fieldContent)               
               if match:
                   return match.group(1).replace(" ", "").upper() 

    def getManufacturer(component):
        manufacturerList = ['Murata', 'AVX', 'Kemet']
        if 'Comment' in component:
            for word in component['Comment'].split():
                for manufacturer in manufacturerList:
                    if manufacturer.lower() == word.lower():
                        return manufacturer
        return ''

    def getDielectricType(component):
        dielectricsList = ['X7R', 'Y5V', 'C0G']
        for field in ['Comment', 'Description']: 
            if field in component:
                for word in component[field].split():
                    for dielectric in dielectricsList:
                        if dielectric.lower() == word.lower():
                            return dielectric
        return ''

    def getManufacturerPartNumber(component):
        capacitorFamilyList = [r'(GCM[A-Za-z0-9]+)', r'C0603', r'C0805']
        for field in ['Comment', 'Description']: 
            if field in component:
                for word in component[field].split():
                    for capacitorRegexpr in capacitorFamilyList:
                        if re.compile(capacitorRegexpr).match(word):
                            return word
        return ''



    part = {}
    part['Capacitance'] = capacitor.farads_to_string(capacitor.convert_capacitance_co_farads(getCapacitance(component)))
    part['Voltage'] = getVoltage(component)
    part['Case'] = getCase(component)
    part['Manufacturer'] = getManufacturer(component)
    part['Manufacturer Part Number'] = getManufacturerPartNumber(component)
    part['Dielectric Type'] = getDielectricType(component)
    part['Quantity'] = getQuantity(component)
    part['Designator'] = component['Designator']
    part['Tolerance'] = getTolerance(component)
    return part
  
def decodeResistor(component):
    def getResistance(component):
        for field in ['Resistance', 'resistance']:
            if field in component:
                if component[field] != '':
                    return component[field].replace(" ", "").replace(",", ".").replace('?', 'R')

        for field in ['Comment', 'Description']:
            fieldContent = component[field].replace(",", ".")
            match = re.search('(\d+(M|k|R|m)\d+)', fieldContent) # try to match 4k7 4R7 4M1 etc.
            if match:
                return match.group(1).replace(" ", "").replace("M", ".").replace("k", ".").replace("R", ".").replace("m", ".") + match.group(2)
            match = re.search(r'(\d+(\.\d+)?[kRM])', fieldContent) # try to match 4.7k 4,7k 4.7M etc.
            if match:
                return match.group(1).replace(" ", "").replace(",", ".")
            match = re.search(r'(\d+(\.\d+)? ?((m|k|M|G)?(O|o)hm))',fieldContent)
            if match:
                if match.group(4) != "":
                    return match.group(1).replace(" ", "").replace(",", ".").replace("Ohm", "").replace("ohm", "").replace('?', 'R')
                else:
                    return match.group(1).replace(" ", "").replace(",", ".").replace("Ohm", "R").replace("ohm", "R").replace('?', 'R')

    def getManufacturer(component):
        manufacturerList = ['Vishay', 'AVX', 'Kemet']
        if 'Comment' in component:
            for word in component['Comment'].split():
                for manufacturer in manufacturerList:
                    if manufacturer.lower() == word.lower():
                        return manufacturer
        return ''

    def getManufacturerPartNumber(component):
        resistorFamilyList = [r'(CRCW[A-Za-z0-9]+)']
        for field in ['Comment', 'Description']: 
            if field in component:
                for word in component[field].split():
                    for resistorRegexpr in resistorFamilyList:
                        if re.compile(resistorRegexpr).match(word):
                            return word
        return ''
                 
    part = {}
    part['Resistance'] = resistor.ohms_to_string(resistor.convert_resistance_to_ohms(getResistance(component)))
    part['Tolerance'] = getTolerance(component)
    part['Case'] = getCase(component)
    part['Manufacturer'] = getManufacturer(component)
    part['Manufacturer Part Number'] = getManufacturerPartNumber(component)
    part['Quantity'] = getQuantity(component)
    part['Designator'] = component['Designator']
    return part

def decodeConnector(component):
    def getManufacturerPartNumber(component):
        if 'Manufacturer Part Number' in component:
            return component['Manufacturer Part Number']
        return ''
    def getManufacturer(component):
        if 'Manufacturer' in component:
            return component['Manufacturer']
        return ''

    connector = {}
    connector['Comment'] = component['Comment']
    connector['Description'] = component['Description']
    connector['Manufacturer'] = getManufacturer(component)
    connector['Manufacturer Part Number'] = getManufacturerPartNumber(component)
    connector['Quantity'] = getQuantity(component)
    connector['Designator'] = component['Designator']
    return connector

def decodeIntegratedCircuit(component):
    def getManufacturerPartNumber(component):
        if 'Manufacturer Part Number' in component:
            return component['Manufacturer Part Number']
        return ''
    def getManufacturer(component):
        manufacturerList = ['ON Semiconductor', 'NXP', 'Texas Instruments', 'Asahi Kasei', 'Bosch', 'STMicroelectronics']
        
        if 'Manufacturer' in component:
            return component['Manufacturer']
        
        if 'Comment' in component:
            for manufacturer in manufacturerList:
                if manufacturer.lower() in component['Comment'].lower():
                    return manufacturer
        return ''
    def removeManufacturerFromComment(component, manufacturer):
        comment = component['Comment'].replace(manufacturer, "")
        return comment.strip()

    ic = {}
    ic['Manufacturer Part Number'] = getManufacturerPartNumber(component)
    ic['Manufacturer'] = getManufacturer(component)
    ic['Comment'] = removeManufacturerFromComment(component, ic['Manufacturer'])
    ic['Description'] = component['Description']        
    ic['Quantity'] = getQuantity(component)
    ic['Designator'] = component['Designator']
    return ic

def loadCSVFile(filename):    
    with open(filename, 'r', encoding='raw_unicode_escape') as csvfile:
        reader = csv.DictReader(csvfile)
        componentList = []
        for row in reader:
     #       row = {k: unicode(v, errors='replace') for k,v in row.iteritems()}
            componentList.append(row)
    return componentList

def saveJsonFile(filename, content):
    print("saving: " + filename)
    import json
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(content, indent=4, sort_keys=True, separators=(',', ': ')))

def removeEmptyFields(component):
    newComponent = {}
    for key in component.keys():
       if component[key] != '':
           newComponent[key] = component[key]
    return newComponent

def process(components):
    capacitors = []
    resistors = []
    inductors = []
    integratedCircuits = []
    connectors = []
    others = []
    for component in components:
        if isCapacitor(component):
            capacitors.append(decodeCapacitor(component))
        elif isResistor(component):
            resistors.append(decodeResistor(component))
        elif isInductor(component):
            inductors.append(component)
        elif isIntegratedCircuit(component):
            integratedCircuits.append(decodeIntegratedCircuit(component))
        elif isConnector(component):
            connectors.append(decodeConnector(component))
        else:
            others.append(removeEmptyFields(component))

    return {'Capacitors': capacitors, 'Resistors': resistors, 'Inductors': inductors, 'IntegratedCircuits': integratedCircuits, 'Connectors': connectors, 'Others': others, 'originalFileContent': components}

def getFilenameFromPath(path):
    import ntpath
    return ntpath.basename(path)

def replaceFileExtension(filename, newExtension):
    import os
    return os.path.splitext(filename)[0] + newExtension

def convert(filename, outputdir):
    print("Converting CSV: " + filename + ", result will be stored in: " + outputdir)
    import os
    components = loadCSVFile(filename)
    fileContent = process(components)
    fileContent['filename'] = filename
    outputFile = replaceFileExtension(getFilenameFromPath(filename), '.json')
    outputFile = os.path.join(outputdir, outputFile)
    saveJsonFile(outputFile, fileContent)

