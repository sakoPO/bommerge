import re

def ohms_to_string(ohms): 
    mul = {'G': 1000000000,
           'M': 1000000,
           'k': 1000,
           'R': 1,
           'm': 0.001,
           'u': 0.000001,
           'n': 0.000000001,
           'p': 0.000000000001,
           'f': 0.000000000000001}
    for key in mul.keys():
        unit = mul[key]
        if ohms >= unit and ohms <= 1000*unit:
            return str(ohms / unit).rstrip('0').rstrip('.') + str(key) 

def murata(partname):
    pass
    
def vishay(partname):
    tolerance = {'D': '0.5%', 'F': '1%', 'J': '5%', 'Z': 'Jumper'}
    tcr = {'K': '100ppm/K', 'N': '200ppm/K', '0': 'Jumper'}

    def string_to_ohms(string):        
        multiply = {'R': 1, 'K': 1000, 'M': 1000000}
        if string == '0000':
            return 0
        match = re.match(r'(\d+)(R|M|K)(\d+)?', string)
        if match:        
            number = int(match.group(1))
            mul = multiply[match.group(2)]
            decimal = int(match.group(3))
            value = number * mul + decimal * (mul / 100)
            return float(value)

            

    match = re.match(r'(CRCW)(0402|0603|0805|1206|1210|1218|2010|2512)([0-9(R|M|K)]{4})(D|F|J|Z)(K|N|0)(E(A|B|C|D|E|F|G|H|K))(HP)?', partname)
    if match:
        print ('Resistor mached: ' + partname)
        resistor = {}
        resistor['Series'] = match.group(1)        
        resistor['Case'] = match.group(2)
        resistor['Resistance'] = ohms_to_string(string_to_ohms(match.group(3)))
        resistor['Tolerance'] = tolerance[match.group(4)]
        resistor['Temperature coefitient'] = tcr[match.group(5)]
        resistor['Manufacturer'] = 'Vishay'
        resistor['Packing'] = match.group(6)
        
        return resistor

    
def resolve(partname):
    component = vishay(partname)
    if component:
        return component    
