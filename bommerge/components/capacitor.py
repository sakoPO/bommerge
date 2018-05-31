from partnameDecoder import capacitors as capacitorResolver

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

