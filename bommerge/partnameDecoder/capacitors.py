import re


def faradsToString(farads):
    mul = {'G': 1000000000,
           'M': 1000000,
           'k': 1000,
           'U': 1,
           'm': 0.001,
           'u': 0.000001,
           'n': 0.000000001,
           'p': 0.000000000001,
           'f': 0.000000000000001}
    for key in mul.keys():
        unit = mul[key]
        if farads >= unit and farads <= 1000*unit:
           if key == 'U':
               return str(farads).rstrip('0').rstrip('.') + 'F'
           else:
               return str(farads / unit).rstrip('0').rstrip('.') + str(key) + 'F'

def capacitanceStringToFarads(string):
    value = int(string[:2])    
    mul = int(string[2])
#    print "value:" + str(value) + ' mul: ' + str(mul)
    return value * 10**mul * 10**-12
    
    



def murata(partname):
    dimension = {'03':'0201', '15': '0402', '18': '0603', '21': '0805', '31': '1206', '32': '1210', '43': '1812', '55': '2220' }
    height = {'3': '0.3mm', '5': '0.5mm', '6': '0.6mm', '8': '0.8mm', '9': '0.85mm', 'A': '1mm', 'B': '1.25mm', 'C': '1.6mm', 'D': '2mm', 'E': '2.5mm', 'M': '1.15mm', 'N': '1.35mm', 'Q': '1.5mm', 'R': '1.8mm', 'X': 'Depends on individual standards'}
    dielectric_type = {'5C': 'C0G', '7U': 'U2J', 'C7': 'X7S', 'R7': 'X7R'}
    voltage = {'0J': '6.3V', '1A': '10V', '1C': '16V', '1E': '25V', 'YA': '35V', '1H': '50V', '2A': '100V', '2E': '250V', '2J': '630V'}
    tolerance = {'C': '+-0.25pF', 'D': '0.5pF', 'J': '5%', 'K': '10%', 'M': '20%'}

    match_GCM_GCJ_series = re.match(r'(GC(J|M))(03|15|18|21|31|32|43|55)(3|5|6|8|9|A|B|C|D|E|M|N|Q|R|X)(5C|7U|C7|R7)(0J|1A|1C|1E|YA|1H|2A|2E|2J)(R\d\d|\dR\d|\d{3}|)(C|D|J|K|M)(.{3})(L|D|K|J|B|C)', partname)
    if match_GCM_GCJ_series:
        match = match_GCM_GCJ_series
        capacitor = {}
        capacitor['series'] = match.group(1)
        capacitor['case'] = dimension[match.group(3)]
        capacitor['height'] = height[match.group(4)]
        capacitor['Dielectric Type'] = dielectric_type[match.group(5)]
        capacitor['Voltage'] = voltage[match.group(6)]
        capacitor['Capacitance'] = faradsToString(capacitanceStringToFarads(match.group(7)))
        capacitor['Tolerance'] = tolerance[match.group(8)]
        capacitor['Manufacturer'] = 'Murata'
        return capacitor

def kemet(partname):
    voltage = {'9': '6.3V', '8': '10V', '4': '16V', '3': '25V', '6': '35V', '5': '50V', '1': '100V', '2': '200V', 'A': '250V'}
    tolerance = {'B': '+-0.10pF', 'C': '0.25pF', 'D': '0.5pF', 'F': '1%', 'G': '2%', 'J': '5%', 'K': '10%', 'M': '20%'}
    
    match = re.match(r'(C)(0201|0402|0603|0805|1206|1210|1808|1812|1825|2220|2225)(C)(\d{3})(B|C|D|F|G|J|K|M)(8|4|3|5|1|2|A)(G)', partname)
    if match:
        print ('Capacitor mached: ' + partname)
        def capacitanceStringToFarads_kamet(string):
            value = int(string[:2])    
            mul = int(string[2])
            if mul == 8:
                return value / 100 * 10**-12
            if mul == 9:
                return value / 10 * 10**-12
            return value * 10**mul * 10**-12
    
        capacitor = {}
        capacitor['series'] = 'C - Standard'
        capacitor['case'] = match.group(2)
        capacitor['Dielectric Type'] = 'C0G'
        capacitor['Voltage'] = voltage[match.group(6)]
        capacitor['Capacitance'] = faradsToString(capacitanceStringToFarads_kamet(match.group(4)))
        capacitor['Tolerance'] = tolerance[match.group(5)]
        capacitor['Manufacturer'] = 'Kemet'
        return capacitor
        
    match = re.match(r'(C)(0201|0402|0603|0805|1206|1210|1808|1812|1825|2220|2225)(C)(\d{3})(J|K|M)(9|8|4|3|6|5|1|2|A)(R)', partname)
    if match:
        print ('Capacitor mached: ' + partname)    
        capacitor = {}
        capacitor['series'] = 'C - Standard'
        capacitor['case'] = match.group(2)
        capacitor['Dielectric Type'] = 'X7R'
        capacitor['Voltage'] = voltage[match.group(6)]
        capacitor['Capacitance'] = faradsToString(capacitanceStringToFarads(match.group(4)))
        capacitor['Tolerance'] = tolerance[match.group(5)]
        capacitor['Manufacturer'] = 'Kemet'
        return capacitor   

        
        
def resolve(partname):
    component = murata(partname)
    if component:
        return component
    component = kemet(partname)
    if component:
        return component
    


