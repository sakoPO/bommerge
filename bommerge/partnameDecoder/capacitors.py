import re
from components import capacitor
from decimal import *
from partnameDecoder import capacitors_murata

def capacitanceStringToFarads(string):
    value = Decimal(string[:2])    
    mul = Decimal(string[2])
    return value * Decimal('10')**mul * Decimal('10')**Decimal('-12')


def kemet(partname):
    voltage = {'9': '6.3V', '8': '10V', '4': '16V', '3': '25V', '6': '35V', '5': '50V', '1': '100V', '2': '200V', 'A': '250V'}
    tolerance = {'B': '+-0.10pF', 'C': '0.25pF', 'D': '0.5pF', 'F': '1%', 'G': '2%', 'J': '5%', 'K': '10%', 'M': '20%'}
    
    match = re.match(r'(C)(0201|0402|0603|0805|1206|1210|1808|1812|1825|2220|2225)(C)(\d{3})(B|C|D|F|G|J|K|M)(8|4|3|5|1|2|A)(G)', partname)
    if match:
        print ('Capacitor mached: ' + partname)
        def capacitanceStringToFarads_kamet(string):
            value = Decimal(string[:2])    
            mul = Decimal(string[2])
            if mul == Decimal(8):
                return value / Decimal(100) * Decimal(10**-12)
            if mul == Decimal(9):
                return value / Decimal(10) * Decimal(10**-12)
            return value * Decimal('10')**mul * Decimal('10')**Decimal('-12')
    
        component = {}
        component['series'] = 'C - Standard'
        component['Case'] = match.group(2)
        component['Dielectric Type'] = 'C0G'
        component['Voltage'] = voltage[match.group(6)]
        component['Capacitance'] = capacitor.farads_to_string(capacitanceStringToFarads_kamet(match.group(4)))
        component['Tolerance'] = tolerance[match.group(5)]
        component['Manufacturer'] = 'Kemet'
        return component
        
    match = re.match(r'(C)(0201|0402|0603|0805|1206|1210|1808|1812|1825|2220|2225)(C)(\d{3})(J|K|M)(9|8|4|3|6|5|1|2|A)(R)', partname)
    if match:
        print ('Capacitor mached: ' + partname)
        component = {}
        component['series'] = 'C - Standard'
        component['Case'] = match.group(2)
        component['Dielectric Type'] = 'X7R'
        component['Voltage'] = voltage[match.group(6)]
        component['Capacitance'] = capacitor.farads_to_string(capacitanceStringToFarads(match.group(4)))
        component['Tolerance'] = tolerance[match.group(5)]
        component['Manufacturer'] = 'Kemet'
        return component   

        
        
def resolve(partname):
    component = capacitors_murata.resolve(partname)
    if component:
        return component
    component = kemet(partname)
    if component:
        return component
    


